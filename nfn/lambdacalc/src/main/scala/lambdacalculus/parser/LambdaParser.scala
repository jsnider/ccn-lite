package lambdacalculus.parser

import scala.util.parsing.combinator.PackratParsers
import scala.util.parsing.combinator.syntactical.StdTokenParsers
import lambdacalculus.parser.ast._

import scala.util.parsing.combinator.lexical.StdLexical
import com.typesafe.scalalogging.slf4j.Logging
import scala.collection.immutable.SortedSet

class LambdaLexer extends StdLexical {
  override def letter = elem("letter", c => (c.isLetter || c == '/') && c != 'λ' && c != '?')
}

class LambdaParser extends StdTokenParsers with PackratParsers with Logging {
  type Tokens = StdLexical
  val lexical =  new LambdaLexer
  val keywords = Set("let", "endlet", "if", "then", "else", "call")
  val unaryLiterals = UnaryOp.values.map(_.toString)
  val binaryLiterals: SortedSet[String] = BinaryOp.values.map(_.toString)

  lexical.delimiters ++= Seq("\\", "λ", "?", ".", "(", ")", "=", ";", "-")
  lexical.reserved ++= keywords ++ binaryLiterals ++ unaryLiterals
  type P[+T] = PackratParser[T]

  val binaryLiteralsToParse = binaryLiterals.map(Parser[String](_)).reduce(_ | _ )
  val unaryLiteralsToParse = unaryLiterals.map(Parser[String](_)).reduce(_ | _ )

  lazy val expr:        P[Expr]       = let | application | notApp
  lazy val notApp:      P[Expr]       = ifthenelse | call | binary | unary | variable | number | lambda | parens

  lazy val lambda:      P[Clos]       = positioned(("λ" | "\\" | "/")  ~> ident ~ ("." ~> expr) ^^ { case name ~ body => Clos(name, body) })
  lazy val application: P[Application]= positioned(expr ~ notApp ^^ { case left ~ right => Application(left, right) })
  lazy val parens:      P[Expr]       = "(" ~> expr <~ ")"
  lazy val variable:    P[Variable]   = positioned(ident ^^ { case name => Variable(name) } )
  lazy val number:      P[Constant]   = negNumber | posNumber
  lazy val negNumber:   P[Constant]   = positioned(numericLit ^^ { case n => Constant(n.toInt) })
  lazy val posNumber:   P[Constant]   = positioned("-" ~> numericLit ^^ {case n => Constant(n.toInt * -1)})
  lazy val let:         P[Let]        = positioned(("let" ~> ident <~ "=") ~ expr ~ ("endlet" ~> expr) ^^
                                                    { case name ~ fun ~ code => Let(name, fun, Some(code))})
  lazy val ifthenelse:  P[IfElse]     = positioned(("if" ~> expr) ~ ("then" ~> expr) ~ ("else" ~> expr) ^^
                                                    { case test ~ thenn ~ otherwise => IfElse(test, thenn, otherwise) })
  lazy val call:       P[Call]      = positioned(("call" ~> numericLit) ~ ident ~ rep(notApp | let) ^^ { case n ~ i ~ exprs=> Call(i, exprs)})

  // TODO take care of left/right evaluation order
  lazy val unary :      P[UnaryExpr]  = positioned( unaryLiteralsToParse ~ notApp ^^ { case lit ~ v => UnaryExpr(UnaryOp.withName(lit), v)})
  lazy val binary:      P[BinaryExpr] = positioned( notApp ~ binaryLiteralsToParse ~ notApp ^^ { case v1 ~ lit ~ v2 => BinaryExpr(BinaryOp.withName(lit), v1, v2)})

  def apply(code: String) = parse(code)

  def parse(code: String):ParseResult[Expr] = {
    logger.info(s"Parsing: $code")
    val tokens = new lexical.Scanner(code.stripLineEnd)
    phrase(expr)(tokens)
  }

//  lazy val defs = repsep(defn, ";") <~ opt(";")
//  lazy val defn = ident ~ "=" ~ expr  ^^ { case name ~ "=" ~ fun => Let(name, fun, None)}
//
//
//  def definitions(str: String): ParseResult[List[Let]] = {
//    logger.info(s"Parsing comand library: $str")
//    val tokens = new lexical.Scanner(str)
//    phrase(defs)(tokens)
//  }
}




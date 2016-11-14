#!/bin/bash
####################################
#
# script for creating fake content objects
#
####################################


# GIVE :Content path
#echo ""
#echo "(1 of 4) Give PATH to content store [DEFAULT: \$CCNL_HOME/test/ndntlv/]:"
#read contentpaht
#if [[ "$contentpaht" == "" ]]; then
	contentpath="$CCNL_HOME/test/ndntlv/"
#fi
# GIVE :Filename
#echo ""
#echo "(2 of 4) Give filename for the content [DEFAULT: mycontent]:"
#read contentname
#if [[ "$contentname" == "" ]]; then
#	contentname="mycontent"
#fi
# GIVE :Prefix
#echo ""
#echo "(3 of 4) Give prefix [DEFAULT: /ccn/test/mycontent]:"
#read prefix
#if [[ "$prefix" == "" ]]; then
#	prefix="/ccn/test/mycontent"
#fi
# GIVE :Content
#echo ""
#echo "(4 of 4) Give content message:"
# echo "poopy poop" | $CCNL_HOME/bin/ccn-lite-mkC -s ccnx2015 "$prefix" > $contentpath$contentname.ccntlv
#$CCNL_HOME/bin/ccn-lite-mkC -s ccnx2015 "/ccn/test/mycontent" > $CCNL_HOME/test/ccntlv/mycontent.ccntlv

#foobar
echo "45" | $CCNL_HOME/bin/ccn-lite-mkC -s ndn2013 "/unoise/foobar/node1/1" > $CCNL_HOME/test/ndntlv/foobar_node1_1.ndntlv

echo "50" | $CCNL_HOME/bin/ccn-lite-mkC -s ndn2013 "/unoise/foobar/node1/2" > $CCNL_HOME/test/ndntlv/foobar_node1_2.ndntlv
	
echo "60" | $CCNL_HOME/bin/ccn-lite-mkC -s ndn2013 "/unoise/foobar/node1/3" > $CCNL_HOME/test/ndntlv/foobar_node1_3.ndntlv

echo "70" | $CCNL_HOME/bin/ccn-lite-mkC -s ndn2013 "/unoise/foobar/node1/4" > $CCNL_HOME/test/ndntlv/foobar_node1_4.ndntlv
#node 2
echo "43" | $CCNL_HOME/bin/ccn-lite-mkC -s ndn2013 "/unoise/foobar/node2/1" > $CCNL_HOME/test/ndntlv/foobar_node2_1.ndntlv

echo "52" | $CCNL_HOME/bin/ccn-lite-mkC -s ndn2013 "/unoise/foobar/node2/2" > $CCNL_HOME/test/ndntlv/foobar_node2_2.ndntlv
	
echo "63" | $CCNL_HOME/bin/ccn-lite-mkC -s ndn2013 "/unoise/foobar/node2/3" > $CCNL_HOME/test/ndntlv/foobar_node2_3.ndntlv

echo "69" | $CCNL_HOME/bin/ccn-lite-mkC -s ndn2013 "/unoise/foobar/node2/4" > $CCNL_HOME/test/ndntlv/foobar_node2_4.ndntlv

#utn
echo "90" | $CCNL_HOME/bin/ccn-lite-mkC -s ndn2013 "/unoise/utn/node1/1" > $CCNL_HOME/test/ndntlv/utn_node1_1.ndntlv
	
echo "60" | $CCNL_HOME/bin/ccn-lite-mkC -s ndn2013 "/unoise/utn/node1/2" > $CCNL_HOME/test/ndntlv/utn_node1_2.ndntlv
	  
echo "40" | $CCNL_HOME/bin/ccn-lite-mkC -s ndn2013 "/unoise/utn/node1/3" > $CCNL_HOME/test/ndntlv/utn_node1_3.ndntlv
	 
echo "20" | $CCNL_HOME/bin/ccn-lite-mkC -s ndn2013 "/unoise/utn/node1/4" > $CCNL_HOME/test/ndntlv/utn_node1_4.ndntlv
#node2
echo "85" | $CCNL_HOME/bin/ccn-lite-mkC -s ndn2013 "/unoise/utn/node2/1" > $CCNL_HOME/test/ndntlv/utn_node2_1.ndntlv
	
echo "65" | $CCNL_HOME/bin/ccn-lite-mkC -s ndn2013 "/unoise/utn/node2/2" > $CCNL_HOME/test/ndntlv/utn_node2_2.ndntlv
	  
echo "45" | $CCNL_HOME/bin/ccn-lite-mkC -s ndn2013 "/unoise/utn/node2/3" > $CCNL_HOME/test/ndntlv/utn_node2_3.ndntlv
	 
echo "15" | $CCNL_HOME/bin/ccn-lite-mkC -s ndn2013 "/unoise/utn/node2/4" > $CCNL_HOME/test/ndntlv/utn_node2_4.ndntlv


#rullan	
echo "200" | $CCNL_HOME/bin/ccn-lite-mkC -s ndn2013 "/unoise/rullan/node1/1" > $CCNL_HOME/test/ndntlv/rullan_node1_1.ndntlv

echo "250" | $CCNL_HOME/bin/ccn-lite-mkC -s ndn2013 "/unoise/rullan/node1/2" > $CCNL_HOME/test/ndntlv/rullan_node1_2.ndntlv
	
echo "300" | $CCNL_HOME/bin/ccn-lite-mkC -s ndn2013 "/unoise/rullan/node1/3" > $CCNL_HOME/test/ndntlv/rullan_node1_3.ndntlv
	
echo "400" | $CCNL_HOME/bin/ccn-lite-mkC -s ndn2013 "/unoise/rullan/node1/4" > $CCNL_HOME/test/ndntlv/rullan_node1_4.ndntlv
#node2
echo "180" | $CCNL_HOME/bin/ccn-lite-mkC -s ndn2013 "/unoise/rullan/node2/1" > $CCNL_HOME/test/ndntlv/rullan_node2_1.ndntlv

echo "275" | $CCNL_HOME/bin/ccn-lite-mkC -s ndn2013 "/unoise/rullan/node2/2" > $CCNL_HOME/test/ndntlv/rullan_node2_2.ndntlv
	
echo "280" | $CCNL_HOME/bin/ccn-lite-mkC -s ndn2013 "/unoise/rullan/node2/3" > $CCNL_HOME/test/ndntlv/rullan_node2_3.ndntlv
	
echo "420" | $CCNL_HOME/bin/ccn-lite-mkC -s ndn2013 "/unoise/rullan/node2/4" > $CCNL_HOME/test/ndntlv/rullan_node2_4.ndntlv


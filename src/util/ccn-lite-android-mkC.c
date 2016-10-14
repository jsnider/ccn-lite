/*
 * @f util/ccn-lite-android-mkC.c
 * @b CLI mkContent, write to Stdout
 *
 * Copyright (C) 2013-15, Christian Tschudin, University of Basel
 *
 * Permission to use, copy, modify, and/or distribute this software for any
 * purpose with or without fee is hereby granted, provided that the above
 * copyright notice and this permission notice appear in all copies.
 *
 * THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
 * WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
 * MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
 * ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
 * WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
 * ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
 * OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
 *
 * File history:
 * 2016-10-13  created by Johan Snider
 */

//different suites
 //TODO: maybe these can be taken out
#define USE_SUITE_CCNB
#define USE_SUITE_CCNTLV
#define USE_SUITE_CISTLV
#define USE_SUITE_IOTTLV
#define USE_SUITE_NDNTLV
 
#define USE_HMAC256
#define USE_SIGNATURES

#define NEEDS_PACKET_CRAFTING

//these will be in util
#include "util/ccnl-common.c" 
#include "util/ccnl-crypto.c"


// ----------------------------------------------------------------------

char *private_key_path; //not used in file
char *witness; // used with w flag?

// ----------------------------------------------------------------------

char* ccn-lite-android-mkC(char* suiteStr, char* addr, int port, char* uri, char* body_param)
{
    unsigned char body[64*1024]; //body of content object
    unsigned char out[65*1024]; //this should be the result
    unsigned char *publisher = out; pointer to out
    char *outfname = 0;
    unsigned int chunknum = UINT_MAX, lastchunknum = UINT_MAX;
    int f, len, opt, plen, offs = 0;
    struct ccnl_prefix_s *prefix; //name of content object 
    int suite = CCNL_SUITE_DEFAULT; 
    struct key_s *keys = NULL; //not exactly sure

    static char uri_static[100];

 
       /* not sure about this n.s.a.t
         case 'k':
            keys = load_keys_from_file(optarg);
            break; */
        /* n.s.a.t
        case 'l':
            lastchunknum = atoi(optarg);
            break;
        case 'n':
            chunknum = atoi(optarg);
            break;
        case 'o':
            outfname = optarg;
            break;
        */

        /* nsat    
        case 'p':
            publisher = (unsigned char*) optarg;
            plen = unescape_component((char*) publisher);
            if (plen != 32) {
                DEBUGMSG(ERROR,
                  "publisher key digest has wrong length (%d instead of 32)\n",
                  plen);
                exit(-1);
            }
            break;
            */
        //case 's':
           // this we need!
            suite = ccnl_str2suite(suiteStr);
            if (!ccnl_isSuite(suite)) {
                return "Suite is not valid\n";
            }
        /* nsat
        case 'w':
            witness = optarg;
            break;
            */
    //put content parameter to 
    body = body_param; //maybe unneccassary

    memset(out, 0, sizeof(out)); //writes zeros to out??

    //set content object name
    strcpy(uri_static, uri); 
    prefix = ccnl_URItoPrefix(uri_static, suite, NULL, NULL); //could have had chunk things here

    if (!prefix) {
        return "no URI found, aborting\n";
    }

    //this function takes prefix, body and length, something and builds the result into string object "out"
    //TODO: fix length
    //for CCNL_SUITE_CCNB
    //len = ccnl_ccnb_fillContent(prefix, body, len, NULL, out);

    //from USE_SUITE_CCNTLV
    
    len = ccnl_ccntlv_prependContentWithHdr(prefix, body, len, NULL, NULL , &offs, out);

    /*switch (suite) {
#ifdef USE_SUITE_CCNB
    case CCNL_SUITE_CCNB:
        len = ccnl_ccnb_fillContent(prefix, body, len, NULL, out);
        break;
#endif
#ifdef USE_SUITE_CCNTLV
    case CCNL_SUITE_CCNTLV:

        offs = CCNL_MAX_PACKET_SIZE;
        if (keys) {
            unsigned char keyval[64];
            unsigned char keyid[32];
            // use the first key found in the key file
            ccnl_hmac256_keyval(keys->key, keys->keylen, keyval);
            ccnl_hmac256_keyid(keys->key, keys->keylen, keyid);
            len = ccnl_ccntlv_prependSignedContentWithHdr(prefix, body, len,
                  lastchunknum == UINT_MAX ? NULL : &lastchunknum,
                  NULL, keyval, keyid, &offs, out);
        } else
            len = ccnl_ccntlv_prependContentWithHdr(prefix, body, len,
                          lastchunknum == UINT_MAX ? NULL : &lastchunknum,
                          NULL , &offs, out);
        break;
#endif
#ifdef USE_SUITE_CISTLV
    case CCNL_SUITE_CISTLV:
        offs = CCNL_MAX_PACKET_SIZE;
        len = ccnl_cistlv_prependContentWithHdr(prefix, body, len,
                  lastchunknum == UINT_MAX ? NULL : &lastchunknum,
                  NULL, &offs, out);
        break;
#endif
#ifdef USE_SUITE_IOTTLV
    case CCNL_SUITE_IOTTLV:
        offs = CCNL_MAX_PACKET_SIZE;
        if (ccnl_iottlv_prependReply(prefix, body, len, &offs, NULL,
                   lastchunknum == UINT_MAX ? NULL : &lastchunknum, out) < 0
              || ccnl_switch_prependCoding(CCNL_ENC_IOT2014, &offs, out) < 0)
            return -1;
        len = CCNL_MAX_PACKET_SIZE - offs;
        break;
#endif
#ifdef USE_SUITE_NDNTLV
    case CCNL_SUITE_NDNTLV:
        offs = CCNL_MAX_PACKET_SIZE;
        if (keys) {
            unsigned char keyval[64];
            unsigned char keyid[32];
            // use the first key found in the key file
            ccnl_hmac256_keyval(keys->key, keys->keylen, keyval);
            ccnl_hmac256_keyid(keys->key, keys->keylen, keyid);
            len = ccnl_ndntlv_prependSignedContent(prefix, body, len,
                  lastchunknum == UINT_MAX ? NULL : &lastchunknum,
                  NULL, keyval, keyid, &offs, out);
        } else {
            len = ccnl_ndntlv_prependContent(prefix, body, len,
                  NULL, lastchunknum == UINT_MAX ? NULL : &lastchunknum,
                  &offs, out);
        }
        break;
#endif
    default:
        break;
    } */

    if (outfname) {
        f = creat(outfname, 0666);
        if (f < 0)
            perror("file open:");
    } else
        f = 1;
    write(f, out + offs, len);
    close(f);

    return 0;
}

// eof

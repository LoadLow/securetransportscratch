# -*- coding: utf-8 -*-
"""
CFFI API for SecureTransport.
"""

from cffi import FFI
ffibuilder = FFI()

ffibuilder.set_source(
    "_securetransport",
    """
    #include <stdlib.h>
    #include <Security/SecCertificate.h>
    #include <Security/SecTrust.h>
    #include <Security/SecureTransport.h>
    """,
    extra_link_args=['-framework', 'Security', '-framework', 'CoreFoundation'],
)

ffibuilder.cdef(
    """
    typedef bool Boolean;
    typedef uint8_t UInt8;
    typedef uint32_t UInt32;
    typedef signed long OSStatus;
    typedef signed long long CFIndex;
    typedef ... *CFArrayRef;
    typedef ... *CFDataRef;
    typedef ... *CFAllocatorRef;
    typedef ... *SSLContextRef;
    typedef ... *SecCertificateRef;
    typedef ... *SecTrustRef;
    typedef ... *CFMutableArrayRef;
    typedef const void *SSLConnectionRef;
    typedef const void *CFTypeRef;

    typedef struct {
        ...;
    } CFArrayCallBacks;

    typedef uint32_t SecTrustResultType;
    enum {
        kSecTrustResultInvalid,
        kSecTrustResultProceed,
        kSecTrustResultDeny,
        kSecTrustResultUnspecified,
        kSecTrustResultRecoverableTrustFailure,
        kSecTrustResultFatalTrustFailure,
        kSecTrustResultOtherError
    };

    const CFAllocatorRef kCFAllocatorDefault;
    const CFArrayCallBacks kCFTypeArrayCallBacks;

    CFMutableArrayRef CFArrayCreateMutable(CFAllocatorRef allocator,
                                           CFIndex capacity,
                                           const CFArrayCallBacks *callBacks);
    void CFArrayAppendValue(CFMutableArrayRef, const void *);

    CFDataRef CFDataCreate(CFAllocatorRef, const UInt8 *, CFIndex);

    SecCertificateRef SecCertificateCreateWithData(CFAllocatorRef, CFDataRef);

    OSStatus SecTrustSetAnchorCertificates(SecTrustRef trust, CFArrayRef anchorCertificates);
    OSStatus SecTrustSetAnchorCertificatesOnly(SecTrustRef trust, Boolean anchorCertificatesOnly);
    OSStatus SecTrustEvaluate(SecTrustRef trust, SecTrustResultType *result);

    typedef enum {
        kSSLServerSide,
        kSSLClientSide
    } SSLProtocolSide;

    typedef enum {
        kSSLStreamType,
        kSSLDatagramType
    } SSLConnectionType;

    typedef enum {
        kSSLSessionOptionBreakOnServerAuth,
        kSSLSessionOptionBreakOnCertRequested,
        kSSLSessionOptionBreakOnClientAuth,
        kSSLSessionOptionFalseStart,
        kSSLSessionOptionSendOneByteRecord
    } SSLSessionOption;

    typedef enum {
        kNeverAuthenticate,
        kAlwaysAuthenticate,
        kTryAuthenticate
    } SSLAuthenticate;

    typedef enum {
        kSSLIdle,
        kSSLHandshake,
        kSSLConnected,
        kSSLClosed,
        kSSLAborted
    } SSLSessionState;

    typedef enum {
        kSSLProtocolUnknown = 0,
        kSSLProtocol3       = 2,
        kTLSProtocol1       = 4,
        kTLSProtocol11      = 7,
        kTLSProtocol12      = 8,
        kDTLSProtocol1      = 9,
        /* DEPRECATED on iOS */
        kSSLProtocol2       = 1,
        kSSLProtocol3Only   = 3,
        kTLSProtocol1Only   = 5,
        kSSLProtocolAll     = 6,
    } SSLProtocol;

    typedef UInt32 SSLCipherSuite;
    enum
    {
       SSL_NULL_WITH_NULL_NULL =               0x0000,
       SSL_RSA_WITH_NULL_MD5 =                 0x0001,
       SSL_RSA_WITH_NULL_SHA =                 0x0002,
       SSL_RSA_EXPORT_WITH_RC4_40_MD5 =        0x0003,
       SSL_RSA_WITH_RC4_128_MD5 =              0x0004,
       SSL_RSA_WITH_RC4_128_SHA =              0x0005,
       SSL_RSA_EXPORT_WITH_RC2_CBC_40_MD5 =    0x0006,
       SSL_RSA_WITH_IDEA_CBC_SHA =             0x0007,
       SSL_RSA_EXPORT_WITH_DES40_CBC_SHA =     0x0008,
       SSL_RSA_WITH_DES_CBC_SHA =              0x0009,
       SSL_RSA_WITH_3DES_EDE_CBC_SHA =         0x000A,
       SSL_DH_DSS_EXPORT_WITH_DES40_CBC_SHA =  0x000B,
       SSL_DH_DSS_WITH_DES_CBC_SHA =           0x000C,
       SSL_DH_DSS_WITH_3DES_EDE_CBC_SHA =      0x000D,
       SSL_DH_RSA_EXPORT_WITH_DES40_CBC_SHA =  0x000E,
       SSL_DH_RSA_WITH_DES_CBC_SHA =           0x000F,
       SSL_DH_RSA_WITH_3DES_EDE_CBC_SHA =      0x0010,
       SSL_DHE_DSS_EXPORT_WITH_DES40_CBC_SHA = 0x0011,
       SSL_DHE_DSS_WITH_DES_CBC_SHA =          0x0012,
       SSL_DHE_DSS_WITH_3DES_EDE_CBC_SHA =     0x0013,
       SSL_DHE_RSA_EXPORT_WITH_DES40_CBC_SHA = 0x0014,
       SSL_DHE_RSA_WITH_DES_CBC_SHA =          0x0015,
       SSL_DHE_RSA_WITH_3DES_EDE_CBC_SHA =     0x0016,
       SSL_DH_anon_EXPORT_WITH_RC4_40_MD5 =    0x0017,
       SSL_DH_anon_WITH_RC4_128_MD5 =          0x0018,
       SSL_DH_anon_EXPORT_WITH_DES40_CBC_SHA = 0x0019,
       SSL_DH_anon_WITH_DES_CBC_SHA =          0x001A,
       SSL_DH_anon_WITH_3DES_EDE_CBC_SHA =     0x001B,
       SSL_FORTEZZA_DMS_WITH_NULL_SHA =        0x001C,
       SSL_FORTEZZA_DMS_WITH_FORTEZZA_CBC_SHA =0x001D,

       /* TLS addenda using AES,
       per RFC 3268 */
       TLS_RSA_WITH_AES_128_CBC_SHA      =     0x002F,
       TLS_DH_DSS_WITH_AES_128_CBC_SHA   =     0x0030,
       TLS_DH_RSA_WITH_AES_128_CBC_SHA   =     0x0031,
       TLS_DHE_DSS_WITH_AES_128_CBC_SHA  =     0x0032,
       TLS_DHE_RSA_WITH_AES_128_CBC_SHA  =     0x0033,
       TLS_DH_anon_WITH_AES_128_CBC_SHA  =     0x0034,
       TLS_RSA_WITH_AES_256_CBC_SHA      =     0x0035,
       TLS_DH_DSS_WITH_AES_256_CBC_SHA   =     0x0036,
       TLS_DH_RSA_WITH_AES_256_CBC_SHA   =     0x0037,
       TLS_DHE_DSS_WITH_AES_256_CBC_SHA  =     0x0038,
       TLS_DHE_RSA_WITH_AES_256_CBC_SHA  =     0x0039,
       TLS_DH_anon_WITH_AES_256_CBC_SHA  =     0x003A,

       /* ECDSA addenda,
       RFC 4492 */
       TLS_ECDH_ECDSA_WITH_NULL_SHA           =    0xC001,
       TLS_ECDH_ECDSA_WITH_RC4_128_SHA        =    0xC002,
       TLS_ECDH_ECDSA_WITH_3DES_EDE_CBC_SHA   =    0xC003,
       TLS_ECDH_ECDSA_WITH_AES_128_CBC_SHA    =    0xC004,
       TLS_ECDH_ECDSA_WITH_AES_256_CBC_SHA    =    0xC005,
       TLS_ECDHE_ECDSA_WITH_NULL_SHA          =    0xC006,
       TLS_ECDHE_ECDSA_WITH_RC4_128_SHA       =    0xC007,
       TLS_ECDHE_ECDSA_WITH_3DES_EDE_CBC_SHA  =    0xC008,
       TLS_ECDHE_ECDSA_WITH_AES_128_CBC_SHA   =    0xC009,
       TLS_ECDHE_ECDSA_WITH_AES_256_CBC_SHA   =    0xC00A,
       TLS_ECDH_RSA_WITH_NULL_SHA             =    0xC00B,
       TLS_ECDH_RSA_WITH_RC4_128_SHA          =    0xC00C,
       TLS_ECDH_RSA_WITH_3DES_EDE_CBC_SHA     =    0xC00D,
       TLS_ECDH_RSA_WITH_AES_128_CBC_SHA      =    0xC00E,
       TLS_ECDH_RSA_WITH_AES_256_CBC_SHA      =    0xC00F,
       TLS_ECDHE_RSA_WITH_NULL_SHA            =    0xC010,
       TLS_ECDHE_RSA_WITH_RC4_128_SHA         =    0xC011,
       TLS_ECDHE_RSA_WITH_3DES_EDE_CBC_SHA    =    0xC012,
       TLS_ECDHE_RSA_WITH_AES_128_CBC_SHA     =    0xC013,
       TLS_ECDHE_RSA_WITH_AES_256_CBC_SHA     =    0xC014,
       TLS_ECDH_anon_WITH_NULL_SHA            =    0xC015,
       TLS_ECDH_anon_WITH_RC4_128_SHA         =    0xC016,
       TLS_ECDH_anon_WITH_3DES_EDE_CBC_SHA    =    0xC017,
       TLS_ECDH_anon_WITH_AES_128_CBC_SHA     =    0xC018,
       TLS_ECDH_anon_WITH_AES_256_CBC_SHA     =    0xC019,


       /* TLS 1.2 addenda,
       RFC 5246 */

       /* Initial state. */
       TLS_NULL_WITH_NULL_NULL                   = 0x0000,

       /* Server provided RSA certificate for key exchange. */
       TLS_RSA_WITH_NULL_MD5                     = 0x0001,
       TLS_RSA_WITH_NULL_SHA                     = 0x0002,
       TLS_RSA_WITH_RC4_128_MD5                  = 0x0004,
       TLS_RSA_WITH_RC4_128_SHA                  = 0x0005,
       TLS_RSA_WITH_3DES_EDE_CBC_SHA             = 0x000A,
       TLS_RSA_WITH_NULL_SHA256                  = 0x003B,
       TLS_RSA_WITH_AES_128_CBC_SHA256           = 0x003C,
       TLS_RSA_WITH_AES_256_CBC_SHA256           = 0x003D,

       /* Server-authenticated (and optionally client-authenticated ) Diffie-Hellman. */
       TLS_DH_DSS_WITH_3DES_EDE_CBC_SHA          = 0x000D,
       TLS_DH_RSA_WITH_3DES_EDE_CBC_SHA          = 0x0010,
       TLS_DHE_DSS_WITH_3DES_EDE_CBC_SHA         = 0x0013,
       TLS_DHE_RSA_WITH_3DES_EDE_CBC_SHA         = 0x0016,
       TLS_DH_DSS_WITH_AES_128_CBC_SHA256        = 0x003E,
       TLS_DH_RSA_WITH_AES_128_CBC_SHA256        = 0x003F,
       TLS_DHE_DSS_WITH_AES_128_CBC_SHA256       = 0x0040,
       TLS_DHE_RSA_WITH_AES_128_CBC_SHA256       = 0x0067,
       TLS_DH_DSS_WITH_AES_256_CBC_SHA256        = 0x0068,
       TLS_DH_RSA_WITH_AES_256_CBC_SHA256        = 0x0069,
       TLS_DHE_DSS_WITH_AES_256_CBC_SHA256       = 0x006A,
       TLS_DHE_RSA_WITH_AES_256_CBC_SHA256       = 0x006B,

       /* Completely anonymous Diffie-Hellman */
       TLS_DH_anon_WITH_RC4_128_MD5              = 0x0018,
       TLS_DH_anon_WITH_3DES_EDE_CBC_SHA         = 0x001B,
       TLS_DH_anon_WITH_AES_128_CBC_SHA256       = 0x006C,
       TLS_DH_anon_WITH_AES_256_CBC_SHA256       = 0x006D,

       /* Addendum from RFC 4279,
       TLS PSK */

       TLS_PSK_WITH_RC4_128_SHA                  = 0x008A,
       TLS_PSK_WITH_3DES_EDE_CBC_SHA             = 0x008B,
       TLS_PSK_WITH_AES_128_CBC_SHA              = 0x008C,
       TLS_PSK_WITH_AES_256_CBC_SHA              = 0x008D,
       TLS_DHE_PSK_WITH_RC4_128_SHA              = 0x008E,
       TLS_DHE_PSK_WITH_3DES_EDE_CBC_SHA         = 0x008F,
       TLS_DHE_PSK_WITH_AES_128_CBC_SHA          = 0x0090,
       TLS_DHE_PSK_WITH_AES_256_CBC_SHA          = 0x0091,
       TLS_RSA_PSK_WITH_RC4_128_SHA              = 0x0092,
       TLS_RSA_PSK_WITH_3DES_EDE_CBC_SHA         = 0x0093,
       TLS_RSA_PSK_WITH_AES_128_CBC_SHA          = 0x0094,
       TLS_RSA_PSK_WITH_AES_256_CBC_SHA          = 0x0095,

       /* RFC 4785 - Pre-Shared Key (PSK ) Ciphersuites with NULL Encryption */

       TLS_PSK_WITH_NULL_SHA                     = 0x002C,
       TLS_DHE_PSK_WITH_NULL_SHA                 = 0x002D,
       TLS_RSA_PSK_WITH_NULL_SHA                 = 0x002E,

       /* Addenda from rfc 5288 AES Galois Counter Mode (GCM ) Cipher Suites
       for TLS. */
       TLS_RSA_WITH_AES_128_GCM_SHA256           = 0x009C,
       TLS_RSA_WITH_AES_256_GCM_SHA384           = 0x009D,
       TLS_DHE_RSA_WITH_AES_128_GCM_SHA256       = 0x009E,
       TLS_DHE_RSA_WITH_AES_256_GCM_SHA384       = 0x009F,
       TLS_DH_RSA_WITH_AES_128_GCM_SHA256        = 0x00A0,
       TLS_DH_RSA_WITH_AES_256_GCM_SHA384        = 0x00A1,
       TLS_DHE_DSS_WITH_AES_128_GCM_SHA256       = 0x00A2,
       TLS_DHE_DSS_WITH_AES_256_GCM_SHA384       = 0x00A3,
       TLS_DH_DSS_WITH_AES_128_GCM_SHA256        = 0x00A4,
       TLS_DH_DSS_WITH_AES_256_GCM_SHA384        = 0x00A5,
       TLS_DH_anon_WITH_AES_128_GCM_SHA256       = 0x00A6,
       TLS_DH_anon_WITH_AES_256_GCM_SHA384       = 0x00A7,

       /* RFC 5487 - PSK with SHA-256/384 and AES GCM */
       TLS_PSK_WITH_AES_128_GCM_SHA256           = 0x00A8,
       TLS_PSK_WITH_AES_256_GCM_SHA384           = 0x00A9,
       TLS_DHE_PSK_WITH_AES_128_GCM_SHA256       = 0x00AA,
       TLS_DHE_PSK_WITH_AES_256_GCM_SHA384       = 0x00AB,
       TLS_RSA_PSK_WITH_AES_128_GCM_SHA256       = 0x00AC,
       TLS_RSA_PSK_WITH_AES_256_GCM_SHA384       = 0x00AD,

       TLS_PSK_WITH_AES_128_CBC_SHA256           = 0x00AE,
       TLS_PSK_WITH_AES_256_CBC_SHA384           = 0x00AF,
       TLS_PSK_WITH_NULL_SHA256                  = 0x00B0,
       TLS_PSK_WITH_NULL_SHA384                  = 0x00B1,

       TLS_DHE_PSK_WITH_AES_128_CBC_SHA256       = 0x00B2,
       TLS_DHE_PSK_WITH_AES_256_CBC_SHA384       = 0x00B3,
       TLS_DHE_PSK_WITH_NULL_SHA256              = 0x00B4,
       TLS_DHE_PSK_WITH_NULL_SHA384              = 0x00B5,

       TLS_RSA_PSK_WITH_AES_128_CBC_SHA256       = 0x00B6,
       TLS_RSA_PSK_WITH_AES_256_CBC_SHA384       = 0x00B7,
       TLS_RSA_PSK_WITH_NULL_SHA256              = 0x00B8,
       TLS_RSA_PSK_WITH_NULL_SHA384              = 0x00B9,


       /* Addenda from rfc 5289  Elliptic Curve Cipher Suites with
       HMAC SHA-256/384. */
       TLS_ECDHE_ECDSA_WITH_AES_128_CBC_SHA256   = 0xC023,
       TLS_ECDHE_ECDSA_WITH_AES_256_CBC_SHA384   = 0xC024,
       TLS_ECDH_ECDSA_WITH_AES_128_CBC_SHA256    = 0xC025,
       TLS_ECDH_ECDSA_WITH_AES_256_CBC_SHA384    = 0xC026,
       TLS_ECDHE_RSA_WITH_AES_128_CBC_SHA256     = 0xC027,
       TLS_ECDHE_RSA_WITH_AES_256_CBC_SHA384     = 0xC028,
       TLS_ECDH_RSA_WITH_AES_128_CBC_SHA256      = 0xC029,
       TLS_ECDH_RSA_WITH_AES_256_CBC_SHA384      = 0xC02A,

       /* Addenda from rfc 5289  Elliptic Curve Cipher Suites with
       SHA-256/384 and AES Galois Counter Mode (GCM ) */
       TLS_ECDHE_ECDSA_WITH_AES_128_GCM_SHA256   = 0xC02B,
       TLS_ECDHE_ECDSA_WITH_AES_256_GCM_SHA384   = 0xC02C,
       TLS_ECDH_ECDSA_WITH_AES_128_GCM_SHA256    = 0xC02D,
       TLS_ECDH_ECDSA_WITH_AES_256_GCM_SHA384    = 0xC02E,
       TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256     = 0xC02F,
       TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384     = 0xC030,
       TLS_ECDH_RSA_WITH_AES_128_GCM_SHA256      = 0xC031,
       TLS_ECDH_RSA_WITH_AES_256_GCM_SHA384      = 0xC032,

       /* RFC 5746 - Secure Renegotiation */
       TLS_EMPTY_RENEGOTIATION_INFO_SCSV         = 0x00FF,

       /*
       * Tags for SSL 2 cipher kinds that are not specified
       * for SSL 3.
       */
       SSL_RSA_WITH_RC2_CBC_MD5 =              0xFF80,
       SSL_RSA_WITH_IDEA_CBC_MD5 =             0xFF81,
       SSL_RSA_WITH_DES_CBC_MD5 =              0xFF82,
       SSL_RSA_WITH_3DES_EDE_CBC_MD5 =         0xFF83,
       SSL_NO_SUCH_CIPHERSUITE =               0xFFFF
    };

    typedef enum {
        kSSLClientCertNone,
        kSSLClientCertRequested,
        kSSLClientCertSent,
        kSSLClientCertRejected
    } SSLClientCertificateState;

    // Error codes
    enum {
        errSSLProtocol              = -9800,
        errSSLNegotiation           = -9801,
        errSSLFatalAlert            = -9802,
        errSSLWouldBlock            = -9803,
        errSSLSessionNotFound       = -9804,
        errSSLClosedGraceful        = -9805,
        errSSLClosedAbort           = -9806,
        errSSLXCertChainInvalid     = -9807,
        errSSLBadCert               = -9808,
        errSSLCrypto                = -9809,
        errSSLInternal              = -9810,
        errSSLModuleAttach          = -9811,
        errSSLUnknownRootCert       = -9812,
        errSSLNoRootCert            = -9813,
        errSSLCertExpired           = -9814,
        errSSLCertNotYetValid       = -9815,
        errSSLClosedNoNotify        = -9816,
        errSSLBufferOverflow        = -9817,
        errSSLBadCipherSuite        = -9818,
        errSSLPeerUnexpectedMsg     = -9819,
        errSSLPeerBadRecordMac      = -9820,
        errSSLPeerDecryptionFail    = -9821,
        errSSLPeerRecordOverflow    = -9822,
        errSSLPeerDecompressFail    = -9823,
        errSSLPeerHandshakeFail     = -9824,
        errSSLPeerBadCert           = -9825,
        errSSLPeerUnsupportedCert   = -9826,
        errSSLPeerCertRevoked       = -9827,
        errSSLPeerCertExpired       = -9828,
        errSSLPeerCertUnknown       = -9829,
        errSSLIllegalParam          = -9830,
        errSSLPeerUnknownCA         = -9831,
        errSSLPeerAccessDenied      = -9832,
        errSSLPeerDecodeError       = -9833,
        errSSLPeerDecryptError      = -9834,
        errSSLPeerExportRestriction = -9835,
        errSSLPeerProtocolVersion   = -9836,
        errSSLPeerInsufficientSecurity = -9837,
        errSSLPeerInternalError     = -9838,
        errSSLPeerUserCancelled     = -9839,
        errSSLPeerNoRenegotiation   = -9840,
        errSSLServerAuthCompleted   = -9841,
        errSSLClientCertRequested   = -9842,
        errSSLHostNameMismatch      = -9843,
        errSSLConnectionRefused     = -9844,
        errSSLDecryptionFail        = -9845,
        errSSLBadRecordMac          = -9846,
        errSSLRecordOverflow        = -9847,
        errSSLBadConfiguration      = -9848,
        errSSLLast                  = -9849     /* end of range, to be deleted */
    };

    typedef OSStatus (*SSLReadFunc) (SSLConnectionRef, void *, size_t *);
    typedef OSStatus (*SSLWriteFunc) (SSLConnectionRef,
                                      const void *,
                                      size_t *);

    void CFRelease (CFTypeRef);

    SSLContextRef SSLCreateContext(CFAllocatorRef,
                                   SSLProtocolSide,
                                   SSLConnectionType);

    OSStatus SSLSetConnection(SSLContextRef, SSLConnectionRef);
    OSStatus SSLGetConnection(SSLContextRef, SSLConnectionRef *);
    OSStatus SSLSetSessionOption(SSLContextRef, SSLSessionOption, Boolean);
    OSStatus SSLGetSessionOption(SSLContextRef, SSLSessionOption, Boolean *);
    OSStatus SSLSetIOFuncs(SSLContextRef,
                           SSLReadFunc,
                           SSLWriteFunc);
    OSStatus SSLSetClientSideAuthenticate(SSLContextRef, SSLAuthenticate);
    OSStatus SSLSetProtocolVersionMax(SSLContextRef context, SSLProtocol maxVersion);
    OSStatus SSLSetProtocolVersionMin(SSLContextRef context, SSLProtocol minVersion);

    OSStatus SSLHandshake(SSLContextRef);
    OSStatus SSLGetSessionState(SSLContextRef, SSLSessionState *);
    OSStatus SSLGetNegotiatedProtocolVersion(SSLContextRef, SSLProtocol *);
    OSStatus SSLSetPeerID(SSLContextRef, const void *, size_t);
    OSStatus SSLGetPeerID(SSLContextRef, const void **, size_t *);
    OSStatus SSLGetBufferedReadSize(SSLContextRef, size_t *);
    OSStatus SSLRead(SSLContextRef, void *, size_t, size_t *);
    OSStatus SSLWrite(SSLContextRef, const void *, size_t, size_t *);
    OSStatus SSLClose(SSLContextRef);

    OSStatus SSLGetNumberSupportedCiphers(SSLContextRef, size_t *);
    OSStatus SSLGetSupportedCiphers(SSLContextRef, SSLCipherSuite *, size_t *);
    OSStatus SSLSetEnabledCiphers(SSLContextRef,
                                  const SSLCipherSuite *,
                                  size_t);
    OSStatus SSLGetNumberEnabledCiphers(SSLContextRef, size_t *);
    OSStatus SSLGetEnabledCiphers(SSLContextRef, SSLCipherSuite *, size_t *);
    OSStatus SSLGetNegotiatedCipher(SSLContextRef, SSLCipherSuite *);
    OSStatus SSLSetDiffieHellmanParams(SSLContextRef, const void *, size_t);
    OSStatus SSLGetDiffieHellmanParams(SSLContextRef, const void **, size_t *);

    OSStatus SSLSetCertificateAuthorities(SSLContextRef, CFTypeRef, Boolean);
    OSStatus SSLCopyCertificateAuthorities(SSLContextRef, CFArrayRef *);

    OSStatus SSLCopyDistinguishedNames(SSLContextRef, CFArrayRef *);
    OSStatus SSLSetCertificate(SSLContextRef, CFArrayRef);
    OSStatus SSLGetClientCertificateState(SSLContextRef,
                                          SSLClientCertificateState *);
    OSStatus SSLCopyPeerTrust(SSLContextRef, SecTrustRef *trust );

    OSStatus SSLSetPeerDomainName(SSLContextRef, const char *, size_t);
    OSStatus SSLGetPeerDomainNameLength(SSLContextRef, size_t *);
    OSStatus SSLGetPeerDomainName(SSLContextRef, char *, size_t *);

    extern "Python" OSStatus python_read_func(SSLConnectionRef,
                                              void *,
                                              size_t*);

    extern "Python" OSStatus python_write_func(SSLConnectionRef,
                                               void *,
                                               size_t*);
""")

if __name__ == "__main__":
    ffibuilder.compile(verbose=True)

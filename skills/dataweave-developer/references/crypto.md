# dw::crypto — Crypto functions

Namespace `dw::Crypto`.
Requires an explicit import: `import * from dw::Crypto`.

Functions: `hashWith`, `HMACBinary`, `HMACWith`, `MD5`, `SHA1`

---

## hashWith

```
hashWith(content: Binary, @CryptographicSink algorithm: String = "SHA-1"): Binary
```

Computes the hash value of binary content using a specified algorithm. The first argument specifies the binary content to use to calculate the hash value, and the second argument specifies the hashing algorithm to use. The second argument must be any of the accepted Algorithm names:

- `content` — The binary input value to hash.
- `algorithm` — The name of the algorithm to use for calculating the hash value of `content`. This value is a string. Defaults to `SHA-1`.

```dataweave
%dw 2.0
import dw::Crypto
output application/json
---
{ "md2" : Crypto::hashWith("hello" as Binary, "MD2") }
```

```json
{ "md2": "\ufffd\u0004ls\ufffd\u00031\ufffdh\ufffd}8\u0004\ufffd\u0006U" }
```

## HMACBinary

```
HMACBinary(secret: Binary, content: Binary, @CryptographicSink algorithm: String = "HmacSHA1"): Binary
```

Computes an HMAC hash (with a secret cryptographic key) on input content. See also, `HMACWith`.

- `secret` — The secret cryptographic key (a binary value) used when encrypting the `content`.
- `content` — The binary input value.
- `algorithm` — The hashing algorithm. `HmacSHA1` is the default. Valid values depend on the JDK version you are using. For JDK 8 and JDK 11, `HmacMD5`, `HmacSHA1`, `HmacSHA224`, `HmacSHA256`, `HmacSHA384`, and `HmacSHA512` are valid algorithms. For JDK 11, `HmacSHA512/224` and `HmacSHA512/256` are also valid.

```dataweave
%dw 2.0
import dw::Crypto
output application/json
---
{
  "HMACBinary" : Crypto::HMACBinary("confidential" as Binary, "xxxxx" as Binary, "HmacSHA512")
}
```

```json
{
  "HMACBinary": "\ufffd\ufffd\ufffd\ufffd^h\ufffd!3\u0005\ufffd֎\u00017\ufffd\ufffd\ufffd`\ufffd8?\ufffdjn7\ufffdbs;\t\ufffdƅ\ufffd\ufffd\ufffdx&g\ufffd~\ufffd\ufffd%\ufffd7>1\ufffdK\u000e@\ufffdC\u0011\ufffdT\ufffd}W"
}
```

## HMACWith

```
HMACWith(secret: Binary, content: Binary, @Since(version = "2.2.0") algorithm: String = "HmacSHA1"): String
```

Computes an HMAC hash (with a secret cryptographic key) on input content, then transforms the result into a lowercase, hexadecimal string. See also, `HMACBinary`.

- `secret` — The secret cryptographic key (a binary value) used when encrypting the `content`.
- `content` — The binary input value.
- `algorithm` — (_Introduced in DataWeave 2.2.0. Supported by Mule 4.2 and later._) The hashing algorithm. By default, `HmacSHA1` is used. Other valid values are `HmacSHA256` and `HmacSHA512`.

```dataweave
%dw 2.0
import dw::Crypto
output application/json
---
{ "HMACWith" : Crypto::HMACWith("secret_key" as Binary, "Some value to hash" as Binary, "HmacSHA256") }
```

```json
{ "HMACWith": "b51b4fe8c4e37304605753272b5b4321f9644a9b09cb1179d7016c25041d1747" }
```

## MD5

```
MD5(content: Binary): String
```

Computes the MD5 hash and transforms the binary result into a hexadecimal lower case string.

- `content` — A binary input value to encrypt.

```dataweave
%dw 2.0
import dw::Crypto
output application/json
---
{ "md5" : Crypto::MD5("asd" as Binary) }
```

```json
{ "md5": "7815696ecbf1c96e6894b779456d330e" }
```

## SHA1

```
SHA1(content: Binary): String
```

Computes the SHA1 hash and transforms the result into a hexadecimal, lowercase string.

- `content` — A binary input value to encrypt.

```dataweave
%dw 2.0
import dw::Crypto
output application/json
---
{ "sha1" : Crypto::SHA1("dsasd" as Binary) }
```

```json
{ "sha1": "2fa183839c954e6366c206367c9be5864e4f4a65" }
```

# Security

> Derived from mulesoft/docs-mule-runtime (BSD 3-Clause).

## Security

It is critical to ensure that the valuable information that a business stores and makes available through software applications and web services is secure, protected from unauthorized users and malicious attackers. But it is also critical that these protected resources, such as credit card information or Social Security numbers, be immediately accessible to authorized, legitimate users and systems to conduct business transactions. +

To provide secure access to information, applications and services can apply a variety of security measures. Mule runtime engine (Mule) provides several tools and methods that enables you to protect applications:

- Securing application configuration properties
- Using the Cryptography module
- Configuring a FIPS 140-2 certified environment
- Securing flows with Spring security
- Configuring TLS cryptographic protocol
- Obtaining access to protected resource using Oath Authorization Grant Types
- Configuring the Mule Secure Token Service

### Secure Configuration Properties

Encrypting configuration properties for your applications involves creating a secure configuration properties file, defining the secure properties in the file, and configuring the file in your project with the Mule Secure Configuration Properties Extension module. +

See details in Secure Configuration Properties

### Cryptography Module

Cryptography Module provides cryptography capabilities to a Mule application. Its main features include:

- Symmetric encryption and decryption of messages.
- Asymmetric encryption and decryption of messages.
- Message signing and signature validation of signed messages.

The module supports these strategies to encrypt and sign your messages:

- JCE +
Provides cryptography capabilities of Java Cryptography Extension.
- PGP +
Provides signing and encryption using Pretty Good Privacy.
- XML +
Provides signing and encryption of XML documents or elements.

For details, refer to Cryptography Module.

### FIPS 140-2 Compliance Support

You can configure Mule 4 to run in a FIPS 140-2 certified environment if you meet the following two requirements:

- A certified cryptography module installed in your Java environment
- Mule settings adjusted to run in FIPS security mode

See details in FIPS 140-2 Compliance Support

### Spring Security

Spring Security provides authentication and authorization via JAAS, LDAP, CAS (Yale Central Authentication service), and DAO. The following topics help get you started securing your flows using Spring Security:

- Configure LDAP Provider for Spring Security +
Perform component authorization, or use it as a Mule security provider.
- Component Authorization Using Spring Security +
Configure authorization using Spring Security features on your Mule components, so that users with different roles can only invoke certain methods.

### TLS Configuration

TLS is a cryptographic protocol that provides communications security for your Mule app. Mule 4.x supports Transport Layer Security (TLS) 1.2 and 1.3.

See details in TLS Configuration

### OAuth Authorization Grant Types

There are four types of authorization grants that an OAuth consumer (a client app) can use to obtain access to a protected resource from an OAuth service provider: Authorization Code, Implicit, Resource Owner Password Credentials, and Client Credentials.

See details in OAuth Authorization Grant Types

### Mule Secure Token Service

Mule supports the OAuth 2.0 protocol. How you configure OAuth 2.0 authorization depends on your OAuth role and objective.

See details in Mule Secure Token Service

## Configure TLS with Keystores and Truststores

TLS is a cryptographic protocol that provides communications security for your Mule app. TLS offers many different ways of exchanging keys for authentication, encrypting data, and guaranteeing message integrity. This topic describes TLS as supported by Mule and how to configure TLS in Mule apps.

### TLS Compatibility Matrix

TLS compatibility differs by Mule deployment model and TLS version.

| TLS Version | On-Premises | CloudHub | Anypoint Runtime Fabric |
|---|---|---|---|
| 1.3 | Supported when running Mule on a JDK that supports TLS 1.3 but _not_ enabled by default | Supported for Mule apps hosted in this deployment model | Supported and enabled when running on a JDK that supports TLS 1.3 |
| 1.2 3+ | Supported and enabled by all deployment models |  |  |

### The tls:context Element

The `tls:context` element is used for all connectors that support TLS. For example, you can configure TLS in HTTP (server and client), FTPS (client), Email (client) or Sockets (client) connectors, among others.

If a connector supports TLS, Studio shows either:

- A **TLS/SSL** tab on that connector's Global Elements Properties.
- A **TLS Configuration** field on the **General** tab of that connector's Global Element Properties.

### The TLS-Enabled Server and Client

A TLS-enabled server contains a private key and a public certificate:

- The private key never leaves the server.
- The public certificate is exposed through TLS.

TLS-enabled clients verify that they trust the server by validating the public certificate against their own set of trusted certificates.

To use TLS communications security in Mule 4, import certificates and private keys into a keystore file. Truststore files are also keystores that by convention include only public certificates of trusted servers.

While there's a default Java truststore, there is no default Java keystore in the standard JRE distribution. Add your own keystore to the TLS context. You likely already have corporate certificates for your client apps and don't need to create them. Often, these certificates work with the JRE truststore, so no setup is required in the TLS context.

A well-known Certificate Authority (CA) can generate certificates, or you can generate a certificate locally without external approval (self-signed certificate). A truststore contains certificates from trusted CAs that the client uses to verify a certificate presented by the server.

### Keystores and Truststores

In a Mule configuration, the `tls:trust-store` and `tls:key-store` elements allow you to reference specific certificates and keys. If you don't specify a `tls:trust-store`, Mule uses the default Java truststore, which is maintained by Java and updated automatically when Java is updated. This helps make sure that certificates from Certificate Authorities (CAs) remain current.

Using a custom Java Trust Store isn't the standard approach in MuleSoft and can lead to connectivity issues with the MuleSoft control plane when MuleSoft certificates are renewed.

Use the default Java truststore to avoid connectivity issues. If you use a custom truststore, you're responsible for managing and updating it.

Truststore and keystore contents differ depending on whether they are used for clients or servers:

- For servers: the truststore contains certificates of the trusted clients, the keystore contains the private and public key of the server.

- For clients: the truststore contains certificates of the trusted servers, the keystore contains the private and public key of the client.

Adding both a keystore and a truststore to the configuration implements two-way TLS authentication also known as mutual authentication.

The keystore contains one or two passwords:

- `password` accesses the entire keystore file.
- `keyPassword` accesses the server's private key inside the keystore.

### Client Configuration

If the `tls:context` has an empty truststore defined, then the default values of the JVM are used, which usually include a truststore with certificates for all the major certifying authorities. Consider the following scenarios:

- When the truststore is defined inline:
```text
<tls:context name>
    <tls:trust-store />
</tls:context>
```

- When the truststore is defined with a global element:
```text
<tls:context name="example">
	<tls:trust-store />
</tls:context>
```

If the client requires a certificate from the server that it is trying to connect to, then add the `tls:trust-store` element. Set `path` to the location within the artifact of the truststore file that contains the certificates of the trusted servers.

If the server validates certificates from the clients, then the `tls:key-store` element should be added with `path` set to the location within the artifact of the keystore file that contains the private/public keys of the client.

See Configure TLS in Mule 4 for configuration instructions.

### Server Configuration

The `tls:context` must contain a `tls:key-store` element to listen for a request using a secure connection such as HTTPS. Set `path` to the location within the artifact of the keystore file that contains the private/public keys of the server.

If the server needs to validate certificates from clients, add a `tls:trust-store` element and set `path` to the location within the artifact of the trust store file that contains the certificates of the trusted clients.

Mule supports many types of keystores, including:

- `JCEKS`
- `PKCS12`
- `JKS`

Specify your keystore type in the JRE.

To fully configure TLS for a Mule app:

1. Generate a keystore and a truststore, using the Java Keytool from Oracle.
1. Configure TLS globally for client or server in Mule.
1. Optional: Specify Protocols and Cipher Suites.

### Keystore Generation

The standard JDK distribution doesn't include a keystore by default, use `keytool` to generate your keystores and certificates. The keystore you generate contains a private key and a public certificate. This certificate is self-signed so it isn't to be trusted by clients unless you share the public certificate with them.

#### Requirements

Use Java 17 to generate your keystores. Using a different JDK version generates an incompatible keystore that causes an invalid keystore format runtime error when the Mule application tries to read the keystore.

#### Generate a Keystore

Follow these steps to generate a keystore and export a self-signed certificate.

1. Generate a keystore that exposes your server's credentials. +
For example, run one of the following commands:
```text
keytool -genkey -keyalg RSA -alias <key-alias> -keystore <keystore-name>.jks

keytool -genkey -alias <key-alias> -keyalg RSA -keystore <keystore-name>.jks -storepass <password>
```

Replace `<key-alias>` with a unique alias of your choice.
Replace `<password>` with a password of your choice.
Replace `<keystore-name>` with the name you want for your keystore.
Optionally, you can set the encryption algorithm to ECDSA by specifying `-keyalg EC` instead of `-keyalg RSA`.
If you don't specify the encryption algorithm, the tool uses DSA by default which isn't compatible with TLS 1.2 and causes the SSL handshake to fail when the Mule app receives an HTTPS request.

1. Respond to the tool's prompts. The following output shows example responses:
```text
Enter keystore password: mule123
Re-enter new password: mule123
```

1. Respond to prompts to enter other values. Enter your desired values. The following output shows example responses:
```text
What is your first and last name?  [Unknown]:  max
What is the name of your organizational unit? [Unknown]:  MuleSoft
What is the name of your organization? [Unknown]:  MuleSoft Inc
What is the name of your City or Locality?  [Unknown]:  San Francisco
What is the name of your State or Province?  [Unknown]:  CA
What is the two-letter country code for this unit?  [Unknown]:  01
```

1. In response to the following prompt, enter: `yes`.
```text
Is CN=max, OU=MuleSoft, O=MuleSoft Inc, L=San Francisco, ST=CA, C=01 correct?  [no]:  yes
```

1. Respond to the following prompt. For example, use the same password by pressing RETURN.
```text
Enter key password for <key-alias>  (RETURN if same as keystore password):
```

1. Enter the following command to export a self-signed certificate authenticating the public key.
```text
keytool -export -alias <key-alias> -keystore <keystore-name>.jks -file <certificate-name>.cer
```

Replace `<key-alias>` with the same value used in the previous steps. +
Replace `<keystore-name>` with the same value used in the previous steps. +
Replace `<certificate-name>` with the name you want for your certificate.

1. Enter the password you set up for the keystore associated with the certificate:
```text
Enter keystore password: mule123
```

#### Request Signing by a Certification Authority

If you want your certificate signed by a Certification Authority (CA), follow these steps:

1. Export your certificate in the standard CSR format. To do so you can run this command:
```text
keytool -certreq -keystore <keystore-name>.jks -alias <key-alias> -file <certificate-name>.csr
```

Replace `<key-alias>` with the same value used in the previous steps. +
Replace `<keystore-name>` with the same value used in the previous steps. +
Replace `<certificate-name>` with the name you want for your certificate sign request file.
1. Send the CSR file generated in the previous step to the Certification Authority and follow their instructions to obtain their signature.

After you receive the CA's signature, you can import the signed certificate file through the following command:
```text
keytool -import -keystore <keystore-name>.jks -alias <cert-alias> -file <signed_certificate_file>
```

Replace `<cert-alias>` with the new desired value. Make sure the alias you define isn't linked to any existing key, or the process fails. +
Replace `<keystore-name>` with the same value used in the previous steps. +
Replace `<signed_certificate_file>` with the name of the signed certificate you received from the Certification Authority.

1. Export your certificate in the standard PEM format. First verify the keystore type, then export the certificates:
```text
keytool -list -v -keystore <keystore-name>.jks
```

```text
openssl <keystore-type> -in <keystore-name>.jks -out <pem-name>.key.pem -nocerts -nodes
openssl <keystore-type> -in <keystore-name>.jks -out <pem-name>.crt.pem -nocerts -nodes
```

Replace `<keystore-type>` with the new desired value in keystore type format, for example PKCS12. +
Replace `<keystore-name>` with the name you want for the keystore. +
Replace `<pem-name>` with the name you want for the PEM file.

### Truststore Generation

The standard JRE distribution includes a default trust store with certificates for several major certificate authorities (CA's) which is used by default in the 'tls:trust-store' element, but you can generate your own if you want greater security or if you use self-signed certificates.

To create a trust store, you can use the Oracle Java keytool.

The client trusts the server if a chain of trust can be established, either directly to the server (in case its certificate is in the truststore) or through a signing CA whose certificate is present in the truststore; otherwise, the connection fails. A trust store must be defined when using self-signed certificates.

### Configure TLS in Mule 4

To enable TLS for Mule apps, configure the `tls:context` element in the Mule XML configuration file in one of three ways:

- Edit the XML file directly.
- Use Anypoint Studio 7.
- Use Design Center.

Whichever method you use, we recommend you review the information in Edit XML to Configure TLS to understand how the attributes of `tls:context` function.

#### Edit XML to Configure TLS

The `tls:context` element defines TLS communication in a Mule app. Unless you have a special requirement, configure TLS globally and then apply it to each specific use, such as listening for or sending HTTPS requests.

##### Globally Define a TLS Element

The `tls:context` element defines a configuration for TLS, which can be used from both the client and server sides. The element can be referenced by other configuration objects of other modules or defined as a nested element of one of them.

Include at least one of the nested elements: key-store and trust-store.

```xml
<tls:context name="customContext">
    <tls:trust-store path="trustStore" password="mulepassword"/>
    <tls:key-store path="clientKeystore" keyPassword="mulepassword" type="pkcs12"
password="mulepassword"/>
 </tls:context>
```

##### Optional Attributes of the `tls-context` Element

Optionally, specify the protocol and cipher suite to enable them:

- `enabledProtocols`: The protocols in the global TLS configuration
- `enabledCipherSuites`: The cipher suites in global TLS configuration

These values are used if there is nothing specified in the global TLS configuration, or if the values are enabled in a global TLS configuration, as described in Optional: Specify Protocols and Cipher Suites.

##### Attributes of the `trust-store` Element

The `password` attribute is required if you specify a `path`. Otherwise, the attributes are optional.

| Attribute | Description |
|---|---|
| `path` | The path to the file within the artifact that contains the trust store. |
| `type` | The type of the trust store. Default is `JKS`. |
| `password` | The trust store password. Required if you specify `path`. |
| `algorithm` | The algorithm the trust store uses. Default is `SunX509`. |
| `insecure` | Boolean that determines whether to validate the trust store. If set to `true`, no validation occurs. Default is `false`. |

Setting `insecure` to `true` renders connections vulnerable to attack. Use it only for prototyping or testing. Never use it in production environments.

##### Attributes of the `key-store` Element

The attributes other than `path` are optional.

| Attribute | Description |
|---|---|
| `path` | The path to the file within the artifact that contains the keystore. Required. |
| `type` | The type of the keystore. Default is `JKS`. |
| `password` | The keystore password. |
| `keyPassword` | The key manager password, which is the password for the private key inside the keystore. |
| `algorithm` | The algorithm used in the keystore. Default is `SunX509`. |

By default, the `path` attribute loads trust and keystore files as classloader resources. For on-premises deployments (hybrid or standalone), set the system property `mule.tlsStores.filesystemLookup.enable` to `true` to enable file system access.

#### Use Design Center to Configure TLS

You can configure TLS for your app in Design Center. For example, to configure TLS in HTTP Listener:

1. Log into Design Center.
1. Open the project.
1. Open HTTP Listener.
1. In the Configuration tab, click **Edit**.
1. In the TLS tab, fill in the TLS Configuration fields as described above.
1. Optionally, fill in the **Enabled Protocols** and **Enabled Cipher Suites** fields as described in Optional: Specify Protocols and Cipher Suites.

Save your configuration and test.

#### Use Anypoint Studio to Configure TLS

You can configure TLS for your app in Anypoint Studio (Studio). For example, to configure TLS in HTTP Listener:

1. Open Studio Center.
1. Open the project.
1. Open HTTP Listener.
1. In the General tab, select an existing configuration or create a new one.
1. In the HTTP Listener config dialog, select the TLS tab.
1. In the TLS tab, choose the TLS Configuration type **Edit Inline**, and supply the values.
1. Optionally, fill in the **Enabled Protocols** and **Enabled Cipher Suites** fields in the Advanced section as described in Optional: Specify Protocols and Cipher Suites.

Save your configuration and test.

### Optional: Specify Protocols and Cipher Suites

When a TLS communication takes place between two systems, a negotiation determines which protocol and cipher suite are used. Optionally, administrators can specify the protocols and cipher suites to use, and then app developers can specify which cipher suites and protocols to use in `tls:context`.

Protocols and cipher suites must be enabled in Mule runtime and individual apps to be used. If the protocols and cipher suites aren't enabled in both places, the default Java environment protocol and cipher suites are used.

To configure protocols and cipher suites in the Mule runtime:

1. The Mule admin edits the `/conf` directory in `$MULE_HOME`. `$MULE_HOME` points to the directory where your Mule installation resides, for example `/opt/mule-4.0`. Select the appropriate file where you specify the cipher suites and protocols:
  - `tls-default.conf` allows fine-tuning when Mule isn't configured to run in Federal Information Processing Standards (FIPS) security mode.
  - `tls-fips140-2.conf` allows fine-tuning when Mule is running in FIPS security mode.
Open the relevant file and comment or uncomment items in the lists to manually configure the allowed cipher suites and TLS protocols. If you make no changes to these files, Mule allows the configured security manager to select cipher suites and protocols for an app.

1. The list of protocols and cipher suites that the admin sets in these configuration files can then be constrained locally by what the app developer specifies in an individual `tls:context` element. The app developer specifies a subset of the configured or default values in the `tls:context` element for use by TLS. Configure the protocols and cipher suites in `enabledProtocols` and `enabledCipherSuites` in the `tls:context` element.

In the `tls:context` element, you can only reference protocols or cipher suites that are included in the Mule global TLS configuration file or defaults. In `tls:context`, set `enabledProtocols` and `enabledCipherSuite` for a Mule app to the value `default`. After these values are set, TLS uses the following protocols and cipher suites:

- Those configured in your global TLS configuration if it exists
- The defaults provided by your Java environment if a global TLS configuration doesn't exist

Cipher suite names can be long and reduce the readability of your XML code. To improve readability, keep these names in an external properties file in your Mule project. You can then reference the properties. For example:

```xml
<tls:context name="serverTlsContext" enabledCipherSuites="${myCipherSuites}" >
```

### Test after deployment Example

```text
time curl -i -k --cert ./<pem-name>.crt.pem --cert-type PEM --key ./<pem-name>.key.pem https://<anypoint-address>:<anypoint-port>
```

Replace `<pem-name>` with the value name defined. +
Replace `<anypoint-address>` with the value name defined by Anypoint Platform. +
Replace `<anypoint-port>` with the value name defined in the Mule application.

### TLS Configuration Examples

You can set up TLS in a Mule XML configuration file for a client or a server.

#### Example: Configuring TLS for a Client

This example secures an FTPS client by setting up a truststore:

```xml
<ftps:config name="ftps">
    <ftps:connection username="anonymous" password="password" host="localhost" port="21" workingDir="/dev">
        <tls:context >
            <tls:trust-store path="trustStore" password="mulepassword" />
        </tls:context>
    </ftps:connection>
</ftps:config>
```

#### Example: Configuring TLS for a Server

This example secures an HTTP listener by setting up a keystore:

```xml
<http:listener-config name="nestedConfig">
    <http:listener-connection protocol="HTTPS" host="localhost" port="8081">
        <tls:context>
            <tls:key-store path="tls/ssltest-keystore.jks" keyPassword="changeit" password="changeit"/>
        </tls:context>
    </http:listener-connection>
</http:listener-config>
```

#### Example: Configuring TLS for Two-Way Authentication

This example sets up two-way authentication (also called mutual authentication), for an HTTP listener:

```xml
<http:listener-config name="nestedConfig">
    <http:listener-connection protocol="HTTPS" host="localhost" port="8081">
        <tls:context>
            <tls:trust-store path="tls/ssltest-cacerts.jks" password="changeit"/>
            <tls:key-store path="tls/ssltest-keystore.jks" keyPassword="changeit" password="changeit"/>
        </tls:context>
    </http:listener-connection>
</http:listener-config>
```

#### Example: Disabling TLS Validations

This example uses the `insecure` property to disable validations for prototyping and development.

Don't use the `insecure` property in production environments.

```xml
<tls:context>
    <tls:trust-store path="tls/ssltest-cacerts.jks" password="changeit" insecure="true"/>
</tls:context>
```

#### Example: Adding Additional Cipher Suites and Protocol Restrictions

This example enables a protocol and cipher suite for an app, assuming a Mule admin has either specified nothing in the global TLS configuration or enabled the cipher suites and protocols being specified here. Use IANA (Internet Assigned Numbers Authority) naming convention for the cipher suites. Check the OpenSSL - IANA mapping for reference.

```xml
<tls:context name="tlsClientContext" enabledProtocols="TLSv1.2" enabledCipherSuites="TLS_DHE_DSS_WITH_AES_128_CBC_SHA256">
    <tls:trust-store path="tls/trustStore" password="mulepassword"/>
</tls:context>
```

## OAuth Authorization Grant Types

There are four types of authorization grants that an OAuth consumer (that is, a client app) can use to obtain access to a protected resource from an OAuth service provider:

- authorization code

- implicit

- resource owner password credentials

- client credentials

For information about the OAuth authorization framework, see RFC 6749, "The OAuth 2.0 Authorization Framework."

For more information about OAuth roles and the OAuth dance, see the Mule Secure Token Service topic.

### Authorization Code

The Authorization Code grant type uses an authorization server (responsible for confirming and granting permission to access the protected resource) and a resource server (responsible for providing access to the protected resource). Though described as independent servers, the authorization and resource servers reside on the same Mule server. With the Authorization Code grant type, a client app must request an authorization code from the service provider before it can request the token that will grant access to protected resources.

The Authorization Code grant type is especially secure, because it authenticates the client and transmits the access token without exposing it to unauthorized parties, including the resource owner.

An OAuth dance that uses an Authorization Code grant type works as follows:

1. Client app wants to use a protected resource controlled by the service provider, so the client initiates a request to access the resource.

1. Client app calls the service provider's authorization server, providing its client ID to confirm that it is a registered client of the service provider.

1. Client app uses a login page supplied by the service provider to authenticate itself to the service provider.

1. After confirming that the client ID is valid (that is, the client app had previously registered with the service provider), and authenticating the resource owner's login credentials, the service provider returns an authorization code.

1. Client app calls the authorization server again, and provides the authorization code, client ID (again), and client secret.

1. Service provider returns an access token.

1. Client app calls the resource server, providing the access token to request the protected resource.

1. Service provider delivers the protected resource.

### Implicit

As with the Authorization Code grant type, an Implicit grant type involves both an authorization server and a resource server. However, rather than taking the extra steps to authenticate a client application by using an authorization code and client secret, the service provider does the following:

- Authenticates a client based upon its client ID.

- Provides the access token to access the protected resource.

The Implicit grant type optimizes performance for browser clients that use a scripting language, such as Javascript. However, this grant type can expose the access token to the resource owner or the resource owner's user-agent.

An OAuth dance that uses an Implicit grant type works as follows:

1. Client app calls the service provider's authorization server, providing its client ID to confirm that it is a registered client of the service provider.

1. Client app uses a login page supplied by the service provider to request that the resource owner authenticate itself to the service provider.

1. After confirming that the client ID is valid (that is, the client app had previously registered with the service provider), and authenticating the resource owner's login credentials, the service provider returns an access token.

1. Client app calls the resource server, providing the access token to request the protected resource.

1. Service provider delivers the protected resource.

### Resource Owner Password Credentials

With the Resource Owner Password Credentials grant type, a client application demands that the resource owner share its service provider login credentials. The client app then uses these credentials to access the service provider and log into the resource owner's account. The service provider accepts the valid login credentials and grants the client app full access to the resource owner's account.

This type of authorization optimizes performance at the expense of sharing secure access credentials. The resource owner must trust the client app not to share access to private data.

An OAuth dance that uses the Resource Owner Password Credentials grant type works as follows:

1. Resource owner provides access credentials to the client app.

1. Client app calls the service provider to request an access token. During the call, the client provides the client ID to confirm that it is a registered client of the service provider. It also provides the access credentials for the protected resource.

1. Service provider authenticates the client app and validates the access credentials. Then it issues an access token.

1. Client app calls the resource server, providing the access token to request access to the protected resource.

1. Service provider delivers the protected resource.

### Client Credentials

With the Client Credentials grant type, a client app requests access to data that is not associated with a particular resource owner. With this grant type, a service provider must only verify that the client as valid. This type of OAuth interaction is sometimes referred to as "two-legged OAuth" because it involves only two roles: the service provider and a client app.  The other three authorization types involve a third role, the resource owner. Thus, they are sometimes referred to as "three-legged OAuth".

The Client Credentials grant type typically applies when the client is also the resource owner.

An OAuth dance that uses the Client Credentials grant type works as follows:

1. Client app calls the authorization server, providing a client ID to confirm that it is a registered client of the service provider.

1. After confirming that the client ID is valid (that is, the client app had previously registered with the service provider), the service provider returns an access token.

1. Client app calls the resource server, providing the access token to request the protected resource.

1. Client app retrieves the protected resource.

## Component Authorization Using Spring Security

Learn how to configure authorization using Spring Security features on your Mule components, so that users with different roles can only invoke certain methods.

### Configure Spring Security Authentication Manager

The Spring Security interface Authentication Manager is responsible for passing requests through a chain of Authentication Provider objects. To secure calls to flow components, you must add the configured `authenticationManager` to the application context.

The following example defines roles with different levels of access to protected processors:

```xml
  <ss:authentication-manager alias="authenticationManager">
    <ss:authentication-provider>
      <ss:user-service id="userService">
        <ss:user name="admin" password="admin" authorities="ROLE_ADMIN" />
        <ss:user name="joe" password="secret" authorities="ROLE_ADMIN" />
        <ss:user name="anon" password="anon" authorities="ROLE_ANON" />
        <ss:user name="user" password="password" authorities="ROLE_ANON" />
        <ss:user name="ross" password="ross" authorities="ROLE_ANON" />
        <ss:user name="marie" password="marie" authorities="ROLE_ANON" />
      </ss:user-service>
    </ss:authentication-provider>
  </ss:authentication-manager>
```

The following example references the previously defined `authenticationManager` to allow only users with `ROLE_ADMIN` roles in the `requiredAuthorities` field to access the operation:

```xml
	<spring:security-manager>
		<spring:delegate-security-provider name="memory-provider" delegate-ref="authenticationManager" />
	</spring:security-manager>

	<flow name="protectedFlow">
		<http:listener doc:name="Listener" config-ref="HTTP_Listener_config" path="/" />
		<http:basic-security-filter doc:name="Basic security filter" realm="mule" />
		<spring:authorization-filter requiredAuthorities="ROLE_ADMIN" />

		<ee:transform doc:name="Transform Message">
			<ee:message>
				<ee:set-payload><![CDATA[%dw 2.0
				output application/json
				---
				{
					"status": "ok"
				}]]>
				</ee:set-payload>
			</ee:message>
		</ee:transform>
	</flow>
```

### Configure Secure Components in Asynchronous Systems

Spring Security is useful for asynchronous systems because to set the authentication on more than one thread you have to add a security property to the security provider.
In the following example, the value `MODE_GLOBAL` is the security property added:

```xml
    <mule-ss:security-manager>
        <mule-ss:delegate-security-provider name="memory-dao" delegate-ref="authenticationManager">
            <mule-ss:security-property name="securityMode" value="MODE_GLOBAL"/>
        </mule-ss:delegate-security-provider>
    </mule-ss:security-manager>
```

## Configure LDAP Provider for Spring Security

In Mule 4, you can either use a Spring Security LDAP provider to perform component authorization, or use it as a Mule security provider via the Spring module. Before you configure the LDAP provider, obtain the Spring JAR files and declare Spring beans.

### Obtain JAR Files

The Mule software distribution provides the Spring JAR files you need in the `<distribution>/lib/opt` directory:

	* `spring-ldap-core-2.3.2.RELEASE.jar`

	* `spring-security-config-4.2.6.RELEASE.jar`

	* `spring-security-core-4.2.6.RELEASE.jar`

	* `spring-security-ldap-4.2.6.RELEASE.jar`

	* `spring-security-web-4.2.6.RELEASE.jar`

### Declare Spring Beans

The DefaultSpringSecurityContextSource class is the access point for obtaining an LDAP context. +
You must declare the Spring bean for `DefaultSpringSecurityContextSource` in a separate `beans.xml` file in your resources folder.

For example, you must set up an LDAP context source for use by the Spring Security authentication provider to search and authenticate your users. Also, you need to define an `authentication-manager` interface with an embedded `ldap-authentication-provider` class as in the following code sample:

```xml
	<beans xmlns="http://www.springframework.org/schema/beans"
	  xmlns:context="http://www.springframework.org/schema/context"
	  xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
	  xmlns:jdbc="http://www.springframework.org/schema/jdbc"
	  xmlns:ss="http://www.springframework.org/schema/security"
	  xsi:schemaLocation="http://www.springframework.org/schema/beans
	  ...
	  http://www.springframework.org/schema/security/spring-security-4.2.xsd">

		<bean id="ldapContextSource" class="org.springframework.security.ldap.DefaultSpringSecurityContextSource">
	        <constructor-arg value="ldap://localhost:389"/>
	        <property name="userDn" value="cn=admin,dc=example,dc=org"/>
	        <property name="password" value="admin"/>
	    </bean>

	    <ss:authentication-manager alias="ldapAuthManager">
			<ss:ldap-authentication-provider
				server-ref="ldapContextSource"
				user-search-base="DC=example,DC=org"
				user-search-filter="(uid={0})"
				group-search-base="DC=example,DC=org"
				group-search-filter="({0})"
				group-role-attribute="ou"
			/>
	    </ss:authentication-manager>

	</beans>
```

### Configure the Mule Security Provider

The `SpringSecurityProviderAdapter` delegates to an `AuthenticationProvider` such as the `LdapAuthenticationProvider`. To configure the Mule security provider review the following example configuration that shows how you can achieve in Mule connector-level security and other security features that require one or more security providers.

```xml
	<spring:config name="Spring_Config" files="beans.xml" />

	<spring:security-manager>
 		<spring:delegate-security-provider name="ldap-provider" delegate-ref="ldapAuthManager" />
	</spring:security-manager>
```

The following example configuration references a basic HTTP security filter:

```xml
	<http:listener-config name="HTTP_Listener_config" doc:name="HTTP Listener config">
		<http:listener-connection host="0.0.0.0" port="8081" />
	</http:listener-config>

	<spring:config name="Spring_Config"  files="beans.xml" />

	<spring:security-manager>
		<spring:delegate-security-provider name="ldap-provider" delegate-ref="ldapAuthManager" />
	</spring:security-manager>

	<flow name="secureFlow">
		<http:listener doc:name="Listener" config-ref="HTTP_Listener_config" path="/test" />

		<http:basic-security-filter doc:name="Basic security filter" securityProviders="#[['ldap-provider']]" realm="mule-realm"/>

		<ee:transform doc:name="Transform Message">
			<ee:message>
				<ee:set-payload><![CDATA[%dw 2.0
					output application/json
					---
					{
						"status": "ok"
					}]]></ee:set-payload>
			</ee:message>
		</ee:transform>
	</flow>
```

### Configure the Component Authorization

To configure the component authorization, declare the `authorization-filter` field as follows:

```xml
	<spring:authorization-filter requiredAuthorities="ROLE_TESTERS" />
```

### See also

- Spring Module
- Component Authorization Using Spring Security
- LDAP Spring Security
- Spring Security Reference

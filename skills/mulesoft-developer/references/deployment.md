# Packaging, Maven and deployment targets

> Derived from mulesoft/docs-mule-runtime (BSD 3-Clause).

## Maven Support in Mule

Mule Maven plugin versions 3.0.0, 3.1.0, 3.1.1, 3.1.2, 3.1.3, 3.1.4, 3.1.5, 3.1.6, 3.1.7, and 3.8.3 are deprecated.

Maven is a project management utility that Mule implements to enhance project development. Mule provides built-in Maven functionality, including the following features:

- Anypoint Exchange
  - Connectors in Anypoint Exchange provide Maven dependency information. In Anypoint Exchange, you can click a connector asset and click **Dependency Snippets** to list the Maven `pom.xml` file dependency.
- Anypoint Studio
  - All new projects created in Anypoint Studio 7 and later are configured with Maven by default. You can run the project with Maven from the command line, or run it directly from Anypoint Studio.
  - You can import an existing Maven project into Anypoint Studio and continue working on it. See Importing and Exporting Projects for more details.
- Mule Runtime Engine
  - You can integrate the packaging, testing, and deployment of your Mule applications with your Maven lifecycle using the Mule Maven plugin.

### Prerequisites

You must be familiar with Maven concepts like managing `pom.xml` files and working with Maven plugins.
If you are just getting started with Maven, we suggest you follow Maven's Getting Started tutorial.

### Benefits

Maven facilitates the management of your Mule applications both inside and outside of Anypoint Studio, providing the following benefits:

- When you create a new Mule project using Anypoint Studio, you can be confident that you are working with the correct Mule project folder structure and the basic set of standard dependencies.
- Anypoint Studio automatically manages your POM file every time you add new elements to your flow that require additional dependencies.
- The Maven POM file makes sharing projects easier and more lightweight because the POM references the dependencies so that you don't have to manually find and include every dependency within the project itself.
- Using Maven to manage the builds ensures that the resulting final build is sanitized and standardized.
- You can program automatic builds using external frameworks such as Bamboo for continuous integration.

### Recommendations

- Use Anypoint Studio to design your applications.
Anypoint Studio's built-in Maven support minimizes the chances that you would have to manually update your POM file with new dependencies as you add to, or modify your applications.

- Update your POM file and `settings.xml` when necessary.
When updating your POM file, the `<packaging>…</packaging>` tag is mandatory. Depending on the type of project you are creating, valid values for this tag are `mule-application`, `mule-domain`, `mule-policy`, and `mule-domain-bundle`. For example, if you create a Mule project using Anypoint Studio, the tag is automatically configured as `<packaging>mule-application</packaging>`.
If you create Maven projects from the command line using archetypes, you need to manage your POM file manually, and in some cases, adjust your `settings.xml` file to point to the MuleSoft Enterprise repository and supply credentials. In some cases, even if you manage your project with Anypoint Studio, you may need to make manual adjustments to your POM as well.

- Use SNAPSHOT version.
SNAPSHOT enables you to identify versions of your project as you work toward producing a stable product to release. For example, you can build a `1.0.0-SNAPSHOT` version of your project, test functionality, make changes, etc. until you are ready to release it as version `1.0.0`. Then you can build upon using a new version, `1.1.0-SNAPSHOT`.
Example XML:
```xml
<groupId>com.mycompany</groupId>
<artifactId>my-application</artifactId>
<version>1.0.0-SNAPSHOT</version>
<packaging>mule-application</packaging>
```

When using Maven for dependency management, use caution when including third-party components in your projects. While MuleSoft maintains a secure repository, we cannot guarantee the safety of components from external sources. Malicious attackers can create fake components and distribute them on third-party repositories. Research and vet all third-party components before incorporating them into your projects. This helps ensure the security and integrity of your applications.

### Configure Your Maven Installation

Even though Anypoint Studio automatically configures Maven to work with Mule when you create a new project, some scenarios require you to manually configure your Maven installation to work with Mule; for example when following continuous integration or continuous deployment (CI/CD) practices.

When you manage your Maven installation, ensure that:

- The `settings.xml` file is properly configured.
  - Configure your Maven preferences in Anypoint Studio to point to your Maven installation.
  - Configure access to MuleSoft repositories.
- The `pom.xml` file is properly configured.
If you update your project outside Studio, keep the `pom.xml` file updated with any necessary adjustments.

For additional information about Maven configuration, see the Maven Reference.

## Mule Maven Plugin

Mule Maven plugin versions 3.0.0, 3.1.0, 3.1.1, 3.1.2, 3.1.3, 3.1.4, 3.1.5, 3.1.6, 3.1.7, and 3.8.3 are deprecated.

The Mule Maven plugin enables you to integrate the packaging and deployment of your Mule applications with your Maven lifecycle. +
See Package a Mule Application for packaging instructions.

The Mule Maven plugin is compatible with Mule runtime engine (Enterprise Edition) and with Mule Kernel (Community Edition).

Using the Mule Maven plugin, you can automate your Mule application deployment to CloudHub, to CloudHub 2.0, to Anypoint Runtime Fabric, or on-premises, using any of the following deployment strategies:

- CloudHub deployment +
Deploys your Mule application to CloudHub. +
See Deploy Applications to CloudHub for instructions.
- CloudHub 2.0 deployment +
Deploys your Mule application to CloudHub 2.0. +
See Deploy Applications to CloudHub 2.0 for instructions.
- Runtime Fabric deployment +
Deploys your Mule application to Anypoint Runtime Fabric. +
See Deploy Applications to Anypoint Runtime Fabric for instructions.
- Runtime Manager REST API deployment +
Deploys your Mule application to your server, or server clusters using the Runtime Manager REST API. +
See Deploy a Mule Application Using the Runtime Manager REST API for instructions.
- Runtime Manager agent deployment +
Deploy your Mule application using the Runtime Manager agent. +
This deployment strategy works only if all your Mule instances reside in one address space. +
See Deploy a Mule Application Using the Runtime Manager Agent for instructions.
- Standalone runtime deployment +
Deploy your Mule application to a Mule instance running on your machine. +
See Deploy a Mule Application to a Standalone Mule Runtime Engine for instructions.

### Compatibility

- Mule 4.x
- Anypoint Studio 7.x

### Mule Maven Plugin Goals

The Mule Maven plugin provides the following goals:

- `package` +
Generates the jar file for your project.
- `deploy` +
Automatically uploads and starts your application in any of the application deployment targets (CloudHub, Runtime Fabric, or On-Premises).
- `mule:deploy` +
Deploys an artifact from the specified location.
- `mule:undeploy` +
Automatically removes your application from any of the application deployment targets (CloudHub, Runtime Fabric, or On-Premises).

Each goal accepts parameters that are unique to the desired plugin behavior.
To provide a parameter from the command line, prepend `-D` to the parameter name.

#### Package Goal

The `package` goal generates the application JAR file. This goal binds by default to the Maven lifecycle phase: `package`.

Optional Parameters
| Name | Type | Description |
|---|---|---|
| `onlyMuleSources` | boolean | Generates the application JAR file containing only the source code. This property is just for sharing purposes. |
| `attachMuleSources` | boolean | Attaches the source code inside the generated JAR file. |
| `lightweightPackage` | boolean | Doesn't generate the repository with all the application dependencies inside the JAR file. This property is just for sharing purposes. |

For example, to execute the `package` goal and set the `attachMuleSources` parameter, you run the following command:
```text
mvn package -DattachMuleSources
```

#### Deploy Goal

This goal uploads and deploys the application JAR file to any of the application deployment targets. The deploy goal binds by default to the Maven lifecycle phase: `deploy`.

Optional Parameters
| Name | Type | Description |
|---|---|---|
| `artifact` | String | Path to the application JAR file to be deployed. By default is set to the application `target` folder. |
| `muleDeploy` | boolean | Instructs the plugin to deploy using the deployment strategy defined in the plugin configuration. If the `muleDeploy` parameter is not set, the plugin uploads the artifacts to the repository defined in the `distributionManagement` section of the application's `pom.xml` file. |

For example, to execute the `deploy` goal and set the `muleDeploy` parameter, you run the following command:
```text
mvn deploy -DmuleDeploy
```

#### mule:deploy Goal

This goal enables you to deploy an artifact without building it. To specify the artifact's location, use the `mule.artifact` parameter.

For example:
```text
mvn mule:deploy -Dmule.artifact=myProject/myArtifact.jar
```

This property is valid for CloudHub, standalone, and on-premises deployments.

#### mule:undeploy Goal

This goal removes an application from any of the application deployment targets. It uses the information from the plugin configuration to remove the application from the defined deployment target.

To execute the `undeploy` goal, run the following command:
```text
mvn mule:undeploy
```

The undeploy goal also deletes the app in Mule Maven plugin 3.3.0 and later versions.

### Add the Mule Maven Plugin to a Mule Project

Before you can perform any operations, you must add the Mule Maven plugin to your project.

To add the Mule Maven plugin, you need to add its maven dependency to the project:

```xml
<plugin>
[source,xml]
```

<groupId>org.mule.tools.maven</groupId>
  <artifactId>mule-maven-plugin</artifactId>
  <version>3.7.1</version>
  <extensions>true</extensions>
```text
</plugin>
```

From this repository:

```xml
<pluginRepositories>
  <pluginRepository>
    <id>mule-public</id>
    <url>https://repository.mulesoft.org/nexus/content/repositories/releases</url>
  </pluginRepository>
</pluginRepositories>
```

This enables the Mule Maven plugin in your project.

If `<extensions>true</extensions>` is not present, the plugin does not work.

### Skip Plugin Execution

You can skip the plugin execution by setting the `skip` parameter to true inside your deployment configuration:

```xml
<plugin>
[source,xml]
```

<groupId>org.mule.tools.maven</groupId>
  <artifactId>mule-maven-plugin</artifactId>
  <version>3.7.1</version>
  <extensions>true</extensions>
```text
  <configuration>
    <standaloneDeployment>
      <muleHome>${mule.home.test}</muleHome>
      <skip>true</skip>
    </standaloneDeployment>
  </configuration>
</plugin>
```

### Skip Deployment Verification

You can skip the status verification of your deployed app by setting the `skipDeploymentVerification` parameter to true inside of any of the platform deployments (Cloudhub, Runtime Manager, and Runtime Fabric):

```xml
<plugin>
[source,xml]
```

<groupId>org.mule.tools.maven</groupId>
  <artifactId>mule-maven-plugin</artifactId>
  <version>3.7.1</version>
  <extensions>true</extensions>
```text
  <configuration>
    <runtimeFabricDeployment>
      ...
      <skipDeploymentVerification>true</skipDeploymentVerification>
      ...
    </runtimeFabricDeployment>
  </configuration>
</plugin>
```

If the `skipDeploymentVerification` parameter is not present, the default value is false. +
This feature is available in plugin version 3.2.5 and later.

### Configure Shared Libraries

Shared libraries enable you to configure a dependency in your application and make this dependency accessible to all the connectors in your application. +
See Shared Libraries for an in-depth explanation of this feature.

To configure a dependency as a shared library, add the following elements inside your Mule Maven plugin configuration in your project's `pom.xml` file:

```xml
<sharedLibraries>
  <sharedLibrary>
    <groupId>${dependencyGroupID}</groupId>
    <artifactId>${dependencyArtifactID}</artifactId>
  </sharedLibrary>
</sharedLibraries>
```

The following example configures Anypoint Connector for Database (Database Connector) in a project, and also configures the MySQL driver as a shared library:

```xml
<build>
  <plugins>
    <!-- Mule Maven Plugin configuration -->
    <plugin>
    	<groupId>org.mule.tools.maven</groupId>
    	<artifactId>mule-maven-plugin</artifactId>
    	<version>${mule.maven.plugin.version}</version>
    	<extensions>true</extensions>
    	<configuration>
    	<sharedLibraries>
        <!-- MySQL driver dependency configured as a shared library -->
        <sharedLibrary>
          <groupId>mysql</groupId>
          <artifactId>mysql-connector-java</artifactId>
        </sharedLibrary>
      </sharedLibraries>
      </configuration>
    </plugin>
  </plugins>
</build>

<dependencies>
  <!--Database Connector dependency -->
  <dependency>
    <groupId>org.mule.connectors</groupId>
    <artifactId>mule-db-connector</artifactId>
    <version>1.5.0</version>
    <classifier>mule-plugin</classifier>
  </dependency>
  <!-- MySQL driver dependency -->
  <dependency>
    <groupId>mysql</groupId>
    <artifactId>mysql-connector-java</artifactId>
    <version>5.1.33</version>
  </dependency>
</dependencies>
```

### Configure Additional Plugin Dependencies

Configuring additional plugin dependencies for a connector in your application makes those dependencies available for only that connector. Doing this  enables you to configure different dependencies, or even multiple versions of the same dependency, for different connectors. +
See Additional Plugin Dependencies for an in-depth explanation of this feature.

To configure additional plugin dependencies, add the following elements inside your Mule Maven plugin configuration in your project's `pom.xml` file:

```xml
<additionalPluginDependencies>
    <plugin>
        <groupId>${connectorGroupID}</groupId>
        <artifactId>${connectorArtifactID}</artifactId>
        <additionalDependencies>
            <dependency>
                <groupId>${dependencyGroupID}</groupId>
                <artifactId>${dependencyArtifactID}</artifactId>
                <version>${dependencyVersion}</version>
            </dependency>
        </additionalDependencies>
    </plugin>
</additionalPluginDependencies>
```

The following example configures the Derby driver as a dependency of Database Connector:

```xml
<plugin>
    <!-- Mule Maven Plugin configuration -->
    <groupId>org.mule.tools.maven</groupId>
    <artifactId>mule-maven-plugin</artifactId>
    <version>${mule.maven.plugin.version}</version>
    <configuration>
        <!-- Plugin dependencies configuration-->
        <additionalPluginDependencies>
            <!-- The connector for which the dependency is defined -->
            <plugin>
                <groupId>org.mule.connectors</groupId>
                <artifactId>mule-db-connector</artifactId>
                <!-- Dependencies definition for the connector -->
                <additionalDependencies>
                    <dependency>
                        <groupId>org.apache.derby</groupId>
                        <artifactId>derby</artifactId>
                        <version>10.11.1.1</version>
                    </dependency>
                </additionalDependencies>
            </plugin>
        </additionalPluginDependencies>
    </configuration>
</plugin>
```

### Mule Maven Plugin Reference

The following links contain the parameter reference of each deployment strategy:

- CloudHub deployment parameters reference
- Runtime Fabric deployment parameters reference
- Standalone deployment parameters reference
- Runtime Manager REST API deployment parameters reference
- Runtime Manager agent deployment parameters reference

## Maven Reference

Mule Maven plugin versions 3.0.0, 3.1.0, 3.1.1, 3.1.2, 3.1.3, 3.1.4, 3.1.5, 3.1.6, 3.1.7, and 3.8.3 are deprecated.

This page summarizes reference information that helps you work when using Maven with Mule. Refer to Maven Support in Mule for an introduction and overview.

### pom.xml File

```xml
<project root>/pom.xml
```

Project Object Model file that defines settings for a Maven project describing an application. It includes all settings necessary to build the application such as build plugin configurations. Note that the `pom.xml` exists on a per-project basis and is distributed along with a project.

### settings.xml File

```xml
<system-wide Maven directory>/settings.xml
<user home directory>/.m2/settings.xml
```

Contains global settings for your Maven installation. Unlike a project's `pom.xml`, it defines system-wide settings and is not distributed with a project, since it can contain confidential information such as authentication credentials.

The `settings.xml` file can reside in two locations:

- In a system-wide settings folder:
In this case, it is a _global_ `settings.xml` file that defines the settings for all Maven installations on the system, regardless of user. For example:
```text
/etc/maven2/settings.xml
```

- In a user-specific settings folder:
In this case, it is a _user_ `settings.xml` file that is relevant only for a specific user's Maven installation. The default location is the `.m2` directory in the user's home directory:
```text
/home/joe/.m2/settings.xml
```

On a system with both global and user `settings.xml` files, the settings from both files become merged. In case there are duplicate settings, the user's settings take precedence over the global settings.

### MuleSoft Repositories

When you create a new Mule project in Anypoint Studio, the required MuleSoft repositories are automatically added to the project. If you create the Mule project outside Studio, you have to manually add the repositories to the `pom.xml` file and also configure your credentials for Maven to access the enterprise repository.

#### Configure MuleSoft Public Repositories

To configure the public MuleSoft repositories, add the following to your project's `pom.xml` file:

```xml
<repositories>
    <repository>
        <id>anypoint-exchange</id>
        <name>Anypoint Exchange</name>
        <url>https://maven.anypoint.mulesoft.com/api/v3/maven</url>
        <layout>default</layout>
    </repository>
    <repository>
        <id>mulesoft-releases</id>
        <name>MuleSoft Releases Repository</name>
        <url>https://repository.mulesoft.org/releases/</url>
        <layout>default</layout>
    </repository>
    <repository>
        <id>mulesoft-public</id>
        <name>MuleSoft Public Repository</name>
        <url>https://repository.mulesoft.org/nexus/content/repositories/public/</url>
        <layout>default</layout>
    </repository>
</repositories>
<pluginRepositories>
    <pluginRepository>
        <id>mulesoft-releases</id>
        <name>MuleSoft Releases Repository</name>
        <layout>default</layout>
        <url>https://repository.mulesoft.org/releases/</url>
        <snapshots>
            <enabled>false</enabled>
        </snapshots>
    </pluginRepository>
</pluginRepositories>
```

#### Configure MuleSoft Enterprise Repository

To add access to the enterprise repository to your project, you must obtain and install an Enterprise license, acquire access to the repository, and configure the repository in your project.

##### Obtain and Install an Enterprise License

See Install an Enterprise License, for instructions to acquire or install an Enterprise license

##### Acquire Access to Enterprise Repositories

If you are a MuleSoft customer and do not have credentials to access the MuleSoft Enterprise repository^, contact Support and request Nexus enterprise credentials.

##### Configure Maven to Access MuleSoft Enterprise Repository

To configure Maven to access the enterprise repository:

1. Navigate to `<USER_HOME>/.m2/settings.xml`.
1. Open `settings.xml` on all workstations that require access. If the `settings.xml` file does not exist, create it.
Read more about the `settings.xml` file in the Maven documentation^.
1. Add the following syntax to the `servers` section in each `settings.xml` file:
```xml
<servers>
...
    <server>

        <id>MuleRepository</id>
        <username>YOUR_ID</username>
        <password>YOUR_PASSWORD</password>

    </server>
...
</servers>
```

1. Add the following syntax to the `profile` section in each `settings.xml` file:
```xml
<profiles>
...
    <profile>

        <id>Mule</id>
        <activation>
            <activeByDefault>true</activeByDefault>
        </activation>
        <repositories>
            <repository>
                <id>MuleRepository</id>
                <name>MuleRepository</name>
                <url>https://repository.mulesoft.org/nexus-ee/content/repositories/releases-ee/</url>
                <layout>default</layout>
                <releases>
                    <enabled>true</enabled>
                </releases>
                <snapshots>
                    <enabled>true</enabled>
                </snapshots>
            </repository>
        </repositories>

    </profile>
...
</profiles>
```

### Useful Commands

The following set of commands enables you to retrieve information about your Maven installation and to perform project-related tasks.

#### Locate the Maven binary and other files (Unix)

```text
whereis mvn
```

#### Locate Maven files such as global configuration files (Unix)

```text
locate maven
```

#### Obtain Maven version

```text
mvn --version
```

This also provides other information such as the Java home directory, locale and processor architecture.

#### Obtain a List of Maven Commands and Options

```text
mvn -h
```

#### Check the Manual Page for Maven (Unix)

```text
man mvn
```

#### Create a Project

```text
mvn archetype:generate -DgroupId=com.company.app -DartifactId=myapp -DarchetypeArtifactId=myarchetypeid -DinteractiveMode=false
```

#### Build a Project

```text
mvn package
```

#### Clean a Project

```text
mvn clean
```

#### Generate a Site

```text
mvn site
```

#### Obtain a List of JAR Files Included in Your Artifact

```text
mvn dependency:build-classpath
```

#### Obtain the Dependency Tree for Your Artifact

```text
mvn dependency:tree
```

### Deploying Mule Artifacts to a Central Maven Repository

Using a central repository can save users' time when building applications. To deploy to a central repository, you need to deploy the Mule `POM` files and `JAR` artifacts to the desired repository.

The deploy plugin is primarily used during the deploy phase, to add your artifacts to a remote repository for sharing with other developers and projects.

#### Deploying pom.xml

To deploy the `pom.xml` to a remote repository, use the following command:

```text
mvn deploy:deploy-file
-DgroupId=${project.groupId}
-DartifactId=${project.artifactId}
-Dversion=${version}
-Dpackaging=pom
-Dfile=${localPom.canonicalPath}
-Durl=http://<your_repository_ip>/nexus/content/repositories/releases
-DrepositoryId=releases
```

For the `-Durl` parameter, replace `<your_repository_ip>` with the correct IP address. Also, the `-DrepositoryId` needs to match with the credentials defined in the `settings.xml` file.

#### Deploying the JAR files

To deploy a `JAR` file to a remote repository, use the following command:

```text
mvn deploy:deploy-file
-DgroupId=${pomProps.groupId}
-DartifactId=${pomProps.artifactId}
-Dversion=${pomProps.version}
-Dpackaging=jar
-Dfile=${f.canonicalPath}
-DpomFile=${localPom.canonicalPath}
-Durl=http://${your_repository_ip}/nexus/content/repositories/releases
-DrepositoryId=releases
```

For the `-Durl` parameter, replace `your_repository_ip` with the correct IP address. Also, the `-DrepositoryId` needs to match with the credentials defined in the `settings.xml` file.

If you wish to both install the `JAR` files locally and deploy them remotely, you can keep both locations in the argument definition.

### External Resources

- Apache Maven Home Page
- Maven Getting Started Guide
- Maven Deploy Plugin Reference
- POM Reference
- Settings Reference

## Deploy Mule Applications

All Mule applications require deployment to a Mule runtime engine instance to run. MuleSoft supports three different deployment targets: CloudHub, Anypoint Runtime Fabric, and on-premises Mule instances.

When you deploy applications to CloudHub or to Anypoint Runtime Fabric, these services automatically manage the Mule runtime engine instances needed to run the applications.

If you deploy applications on-premises, the installation of Mule runtime engine is required. +
See On-Premises Deployment Model for more information about characteristics specific to on-premises deployments.

In addition, different tools are available to deploy applications to each of the deployment targets:

| Deployment Target | Available Deployment Tools | Mule Runtime Engine Installation |
|---|---|---|
| CloudHub |  · Anypoint Code Builder · Anypoint Platform CLI · Anypoint Runtime Manager · Anypoint Studio · Mule Maven plugin |  · No installation of Mule runtime engine is required, because CloudHub workers start Mule instances as part of the deployment process. |
| CloudHub 2.0 |  · Anypoint Code Builder · Anypoint Platform CLI · Anypoint Runtime Manager · Anypoint Studio · Mule Maven plugin |  · No installation of Mule runtime engine is required, because CloudHub 2.0 replicas start Mule instances as part of the deployment process. |
| Anypoint Runtime Fabric |  · Anypoint Runtime Manager · Runtime Manager in Anypoint Platform Private Cloud Edition · Mule Maven plugin |  · No installation of Mule runtime engine is required, because Anypoint Runtime Fabric internally starts Mule instances as part of the deployment process. · Installation of Anypoint Runtime Fabric in your desired infrastructure is required |
| On-premises |  · Anypoint Platform CLI · Anypoint Runtime Manager · Anypoint Studio · Runtime Manager in Anypoint Platform Private Cloud Edition · Mule Maven plugin |  · Installation of Mule runtime engine in your desired infrastructure is required. · You are responsible for the installation and configuration of your Mule instances. |

## Deploy Applications to CloudHub 2.0 Using the Mule Maven Plugin

Mule Maven plugin versions 3.0.0, 3.1.0, 3.1.1, 3.1.2, 3.1.3, 3.1.4, 3.1.5, 3.1.6, 3.1.7, and 3.8.3 are deprecated.

In addition to using Anypoint Runtime Manager, to deploy applications to CloudHub 2.0, you can also deploy applications by using the Mule Maven plugin. To do so, you must meet certain prerequisites, and configure your CloudHub 2.0 deployment strategy in your project's `pom.xml` file.

### Before You Begin

- Ensure that the Mule Maven Plugin is added to your project
See Add the Mule Maven Plugin to a Mule Project for instructions.
- The application is already published in Exchange
See Publish and Deploy Exchange Assets Using Maven.
- The Mule Maven Facade API (v3) is added as a repository in the distribution management section of your project's POM file. For example:
```xml
  <distributionManagement>
    <repository>
      <id>Repository</id>
      <name>Corporate Repository</name>
      <url>https://maven.anypoint.mulesoft.com/api/v3/organizations/ORGANIZATION_ID/maven</url>
      <layout>default</layout>
    </repository>
  </distributionManagement>
```

See The Mule Maven Facade API documentation^ for more information.

### Configure the CloudHub 2.0 Deployment Strategy

Inside the `plugin` element, add a configuration for your CloudHub 2.0 deployment, replacing the following placeholder values with your CloudHub 2.0 information:

```xml
<plugin>
[source,xml]
```

<groupId>org.mule.tools.maven</groupId>
  <artifactId>mule-maven-plugin</artifactId>
  <version>3.7.1</version>
  <extensions>true</extensions>
```text
  <configuration>
    <cloudhub2Deployment>
      <uri>https://anypoint.mulesoft.com</uri>
      <provider>MC</provider>
      <environment>${environment}</environment>
      <target>${targetName}</target>
      <muleVersion>${muleVersion}</muleVersion>
      <username>${user}</username>
      <password>${pass}</password>
      <applicationName>${appName}</applicationName>
      <replicas>1</replicas>
      <vCores>1</vCores>
      <deploymentSettings>
        <http>
          <inbound>
            <publicUrl>${publicUrl}</publicUrl>
            <forwardSslSession>true</forwardSslSession>
            <lastMileSecurity>true</lastMileSecurity>
          </inbound>
        </http>
      </deploymentSettings>
    </cloudhub2Deployment>
  </configuration>
</plugin>
```

### Deploy to CloudHub 2.0

From the command line in your project's folder, package the application and execute the deploy goal:

```sh
mvn clean deploy -DmuleDeploy
```

To deploy the artifact without rebuilding it, run:

```sh
mvn mule:deploy
```

#### Exchange Snapshot Assets

You can also deploy Exchange snapshot assets into CloudHub 2.0.

By using `SNAPSHOT` version assets in Anypoint Exchange during the development and testing phase, you can avoid incrementing your application's version number for small changes. After your `SNAPSHOT` version application has been overwritten in Anypoint Exchange, you can redeploy your `SNAPSHOT` version application to CloudHub 2.0 via the Mule Maven plugin to deploy the latest changes.

To learn more about publishing snapshot assets to Anypoint Exchange, see Asset Lifecycle State.

Each time you update your application's snapshot, redeploy the application to refresh it with the latest snapshot binaries.

Because snapshot assets can change after deployment, avoid deploying them into your production environment.

### Redeploy to CloudHub 2.0

To redeploy the application, run the same command as you did to deploy. +
CloudHub 2.0 rewrites the application you had deployed.

### Authentication Methods

When you deploy applications using Mule Maven plugin, you can use different methods to provide your credentials to authenticate against the deployment platform. Depending on the authentication method you use, the parameters to set in the deployment configuration differ:

| Authentication Method | Description | Configuration Parameters |
|---|---|---|
| Username and password \| Use a CloudHub 2.0 username and password to authenticate. \|* `username` + · `password` | Server \| Use credentials stored in a Maven server, configured inside the Maven `settings.xml` file. \| * `server` | Authorization Token \| Use an authorization token to access the platform. + See Identity Management for a list of supported single sign-on (SSO) types. \|* `authToken` |
| Connected Apps \|Use a Connected App to perform the authentication programmatically by communicating with Anypoint Platform. + Note that the Connected App credentials must have the `Design Center Developer` access scope. + See Connected Apps for Developers for instructions about creating Connected Apps. \|* `connectedAppClientId` + · `connectedAppClientSecret` + · `connectedAppGrantType` |  |  |

For a detailed description of the configuration parameters, see the CloudHub 2.0 Deployment Parameters Reference.

### CloudHub 2.0 Deployment Parameters Reference

| Parameter | Description | Required |
|---|---|---|
| `cloudhub2Deployment` | Top-Level Element | Yes |
| `uri` | Your Anypoint Platform URI. + If not set, defaults to +https://anypoint.mulesoft.com+. \| No | `muleVersion` |
| The Mule runtime engine version to run in your CloudHub 2.0 instance.  + Ensure that this value is equal to or higher than the earliest required Mule version of your application. By default, the latest available Mule version is selected. + Example values: `4.6.0` selects the last build where it defaults to Edge channel and Java 8. If you want to select a different LTS or Edge selection or Java version, specify the full Mule version name as in `4.6.0:1e-java17`. + When using Mule Maven plugin versions 3.8.0 and 4.0.0 for deployments, the `muleVersion` property doesn't allow you to specify `releaseChannel` and `javaVersion`. To specify these properties, upgrade the plugin to version 4.1.1 or later. + Because Mule runtime 4.4 Standard Support ends in October 2024, new Mule apps can be deployed on either Mule 4.6 LTS or Mule 4.8 Edge. As LTS channel isn't supported for customers using a Mule Maven plugin version 4.1.0 or earlier, upgrade the plugin to version 4.1.1 or later. \| No | `releaseChannel` | Set the name of the release channel used to select the Mule image. Supported values are `NONE`, `EDGE`, and `LTS`. By default, the value is set to `EDGE`. If the selected release channel doesn't exist, an error occurs. |
| No | `javaVersion` | Set the Java version used in the deploy. Supported values are `8` and `17`. By default, the value is set to `8`. If the selected Java version doesn't exist, an error occurs. |
| No | `username` | Your Anypoint Platform username |
| Only when using Anypoint Platform credentials to login. | `password` | Your Anypoint Platform password |
| Only when using Anypoint Platform credentials to login. | `applicationName` | The application name displayed in Runtime Manager after the app deploys. |
| Yes | `scopeLoggingConfigurations` |  [cols=".^1,.^1,.^3"] !=== .2+! `scopeLoggingConfiguration` ! `scope` ! The package of the logging library to use. ! `logLevel` ! The log level. Accepted values: `INFO`, `DEBUG`, `WARN`, `ERROR`, `FATAL`. !=== Configuration example: [source,xml,linenums] ---- <scopeLoggingConfigurations> <scopeLoggingConfiguration> <scope>com.pkg.warning</scope> <logLevel>WARN</logLevel> </scopeLoggingConfiguration> <scopeLoggingConfiguration> <scope>com.pkg.debug</scope> <logLevel>DEBUG</logLevel> </scopeLoggingConfiguration> </scopeLoggingConfigurations> ---- |
| No | `target` | The CloudHub 2.0 target name to deploy the app to. + Specify either a shared space or a private space available in your Deployment Target values in CloudHub 2.0. See Features of CloudHub 2.0 for a detailed description on shared and private spaces. Use a target name value from the list of regions. For example, `Cloudhub-US-East-1`. \| Yes |
| `provider` | Provider MC (MuleSoft Control Plane) indicates that the deployment is managed through Anypoint Runtime Manager. Set to `MC` for CloudHub 2.0. | Yes |
| `environment` | Target Anypoint Platform environment. + This value must match an environment configured in your Anypoint Platform account, as shown here: + [source,xml,linenums] ---- <environment>Sandbox</environment> ---- | Yes |
| `replicas` | Specifies the number of replicas, or instances, of the Mule application to deploy. | Only when `autoscaling` is set to `false`. |
| `vCores` | The size of each replica specified in vCores. Accepted values: `0.1`, `0.2`, `0.5`, `1`, `1.5`, `2`, `2.5`, `3`, `3.5`, `4`. See CloudHub 2.0 Replicas for a detailed description of available vCore sizes and their assigned hardware resources. + This parameter cannot be used if you configure `instanceType`. | Yes (Only when `instanceType` isn't configured.) |
| `businessGroup` | The Business group path of the deployment + Specify the full hierarchical path from the parent organization to the target Business group, for example: [source,xml,linenums] ---- <businessGroup>ParentOrg\SubOrg1\myBusinessGroup</businessGroup> ---- This value is omitted if `businessGroupId` is set. If `businessGroup` and `businessGroupId` are not set, the value defaults to the main business group of the user. | No |
| `businessGroupId` | The Business group ID of the deployment + Instead of specifying the Business group path, you can specify the Business group ID to deploy your application. If `businessGroupId` and `businessGroup` are not set, the value defaults to the main business group of the user. + The Business group ID is a mandatory parameter when you have access only to a specific Business group but not to the parent organization. + This parameter is available in plugin version 3.2.7 and later. \| No | `deploymentTimeout` |
| The allowed elapsed time, in milliseconds, between the start of the deployment process and the confirmation that the artifact has been deployed The default value is `600000`. \| No | `server` | Maven server with Anypoint Platform credentials + This is only needed if you want to use your credentials stored in your Maven `settings.xml` file. This is not the Mule server name. \| No |
| `properties` | Top-Level element + If you need to set properties for the Mule application you are deploying, you can use the `<properties>` top-level element: [source,xml,linenums] ---- <properties> <key>value</key> </properties> ---- For example: [source,xml,linenums] ---- <properties> <http.port>8081</http.port> </properties> ---- If you redeploy the application and neither the `properties` nor the `secureProperties` element is configured in the deployment POM file, CloudHub 2.0 preserves the existing properties configured in your CloudHub 2.0 environment. If either element is present, CloudHub 2.0 deploys the application using only the properties and secure properties defined in the POM. It doesn't merge them with values configured in Runtime Manager. Any existing properties that aren't included in the deployment configuration are removed. To keep existing values, omit both elements, or send the full set of properties and secure properties on every redeploy. | No |
| `propertiesFile` | Top-level element + Specifies a file that contains properties for the Mule application being deployed. Use this parameter as an alternative to defining properties inline with `<properties>`. The file must use the Java properties format, with one `key=value` pair per line. \| No | `secureProperties` |
| Top-Level element + Use the `secureProperties` top-level element to set properties for the Mule application and instruct CloudHub 2.0 to encrypt the values before storing them: [source,xml,linenums] ---- <secureProperties> <key>value</key> </secureProperties> ---- For example: [source,xml,linenums] ---- <secureProperties> <http.port>8081</http.port> </secureProperties> ---- If you redeploy the application and neither the `secureProperties` nor the `properties` element is configured in the deployment POM file, CloudHub 2.0 preserves the existing secure properties configured in your CloudHub 2.0 environment. If either element is present, CloudHub 2.0 deploys the application using only the properties and secure properties defined in the POM. It doesn't merge them with values configured in Runtime Manager. Any existing secure properties that aren't included in the deployment configuration are removed. To keep existing values, omit both elements, or send the full set of properties and secure properties on every redeploy. | No | `skip` |
| When set to `true`, skips the plugin deployment goal. + Its default value is `false`. \| No | `skipDeploymentVerification` | When set to `true`, skips the status verification of your deployed app. + Its default value is `false`. \| No |
| `authToken` | Specifies the authorization token to access the platform. You can use this authentication method instead of setting username and password. + See Identity Management for a list of supported single sign-on (SSO) types. \| Only when using an Authorization token to login. | `connectedAppClientId` |
| Specifies the Connected App `clientID` value. | Only when using Connected Apps credentials to login. | `connectedAppClientSecret` |
| Specifies the Connected App secret key. | Only when using Connected Apps credentials to login. | `connectedAppGrantType` |
| Specifies the only supported connection type: `client_credentials`. | Only when using Connected Apps credentials to login. | `deploymentSettings` |
| Any of the parameters documented in deploymentSettings Reference. | No | `integrations` |
|  [cols=".^1,.^1,.^1,.^3"] !=== ! `services` ! `objectStoreV2` ! `enabled` ! When set to `true`, instructs the deployment to use Object Store v2. !=== Configuration example: [source,xml,linenums] ---- <integrations> <services> <objectStoreV2> <enabled>true</enabled> </objectStoreV2> </services> </integrations> ---- | No |  |

#### deploymentSettings Parameters Reference

| Parameter | Description |
|---|---|
| `enforceDeployingReplicasAcrossNodes` | Enforces the deployment of replicas across different nodes. The default value is `false`. + For high availability, set this value to `true`. Configuration example: [source,xml,linenums] ---- <deploymentSettings> <enforceDeployingReplicasAcrossNodes>false</enforceDeployingReplicasAcrossNodes> </deploymentSettings> ---- |
| `updateStrategy` |  [cols=".^1,.^3"] !=== ! Accepted values ! Description ! `rolling` ! Maintains availability by updating replicas incrementally. Requires one additional replica’s worth of resources to succeed. + If `enforceDeployingReplicasAcrossNodes` is enabled, the maximum number of replicas you can configure is one less than the total number of nodes. ! `recreate` ! Terminates replicas before re-deployment. Re-deployment is quicker than `rolling` and doesn’t require additional resources. + If `enforceDeployingReplicasAcrossNodes` is enabled, the maximum number of replicas you can configure is equal to the number of nodes. !=== The default value is `rolling`. Configuration example: [source,xml,linenums] ---- <deploymentSettings> <updateStrategy>recreate</updateStrategy> </deploymentSettings> ---- |
| `clustered` | Enables clustering across two or more replicas of the application. The default value is `false`. + Configuration example: [source,xml,linenums] ---- <deploymentSettings> <clustered>true</clustered> </deploymentSettings> ---- |
| `http` |  [cols=".^1,.^1,.^3"] !=== .5+! `inbound` ! `publicUrl` ! URL of the deployed application. You can add multiple comma-separated values. ! `endpoint` ! Defines application endpoints by specifying the `url`, `pathRewrite`, and `access` attributes. Accepted values for `access` are `internal` and `external`. ! `pathRewrite` ! Supplies the base path expected by the HTTP listener in your application. This value must begin with `/`. This parameter is used only for applications that are deployed to private space. ! `lastMileSecurity` ! Enable Last-Mile security to perform TLS termination and decryption for forwarded HTTPS connections directly within the Mule application. This requires the Mule application to include an SSL certificate and consumes additional CPU resources. The default value is `false`. ! `forwardSslSession` ! Enables SSL forwarding during a session. The default value is `false`. !=== [NOTE] ==== Mule Maven Plugin supports both `publicUrl` and `endpoint` for configuring application endpoints. Configure either `publicUrl` or `endpoints`, but not both in the same deployment configuration. ==== Configuration example: [source,xml,linenums] ---- <deploymentSettings> <http> <inbound> <publicUrl>https://myapp.anypoint.com</publicUrl> <pathRewrite>/api</pathRewrite> <lastMileSecurity>true</lastMileSecurity> <forwardSslSession>true</forwardSslSession> </inbound> </http> </deploymentSettings> ---- Example using `endpoint`: [source,xml,linenums] ---- <deploymentSettings> <http> <inbound> <endpoints> <endpoint> <url>https://test1.com/ch2testapp1</url> <pathRewrite>/</pathRewrite> <access>external</access> </endpoint> </endpoints> </inbound> </http> </deploymentSettings> ---- |
| `generateDefaultPublicUrl` | When set to `true`, CloudHub 2.0 generates a public URL for the deployed application. + This parameter is used only for applications that are deployed to private space. Applications that are deployed to shared space always get a generated public URL. |
| `disableAmLogForwarding` | Disables the application-level log forwarding to Anypoint Monitoring. The default value is `false`. |
| `tracingEnabled` | Exposes tracing information in OpenTelemetry standard from Mule runtime into all APM solutions. See Enable Trace Data Collection. |
| `autoscaling` | Provides CPU based horizontal autoscaling configuration for deployment and redeployment operations. If autoscaling is disabled and the fields `minReplicas` and `maxReplicas` are provided, they must match the value of the `target.replicas` field. See Enable Trace Data Collection. Configuration example: [source,xml,linenums] ---- <deploymentSettings> <autoscaling> <enabled>true</enabled> <minReplicas>1</minReplicas> <maxReplicas>2</maxReplicas> </autoscaling> </deploymentSettings> ---- |
| `instanceType` | Specifies the capacity of the replica for application deployment. This flag is available only for organizations using a usage-based pricing (UBP) package. Non-UBP organizations use the `vCores` parameter instead. See general::pricing. |

### Encrypt Credentials

To use encrypted credentials when deploying, you need to set up your Maven master encrypted password and your `settings-security.xml` file.

1. Create a master password for your Maven configuration.
```text
mvn --encrypt-master-password <yourMasterPassword>
```

Maven returns your master password encrypted:
```text
{l9vZ2uM5SdgHy+H12z4pX7LEOZn3Kbnqmt3kIquLjnQ=}
```

1. Create a `settings-security.xml` file in your ~/.m2 repository and add your encrypted master password:
```xml
<settingsSecurity>
  <master>{l9vZ2uM5SdgHy+H12z4pX7LEOZn3Kbnqmt3kIquLjnQ=}</master>
</settingsSecurity>
```

1. Encrypt your Anypoint platform password:
```text
mvn --encrypt-password <yourAnypointPlatformPassword>
```

Maven returns your Anypoint platform password encrypted:
```text
{HTWFGH5BG9QmvJ1B=}
```

1. Add your encrypted Anypoint Platform password to your `settings.xml` file in the <server> section:
```xml
<settings>
 ...
  <servers>
   ...
    <server>
      <id>my.anypoint.credentials</id>
      <username>my.anypoint.username</username>
      <password>{HTWFGH5BG9QmvJ1B=}</password>
    </server>
   ...
  </servers>
 ...
</settings>
```

1. In your configuration deployment, reference the credentials injecting the server ID configured in your `settings.xml` file:

```xml
<plugin>
  ...
  <configuration>
    ...
    <cloudhub2Deployment>
      ...
      <server>my.anypoint.credentials</server>
      ...
    </cloudhub2Deployment>
    ...
  </configuration>
  ...
<plugin>
```

> **Note:** Make sure that the username and password aren't set in the deployment configuration, or they will overwrite the defined server ID.

## Deploy Applications to Runtime Fabric Using the Mule Maven Plugin

Mule Maven plugin versions 3.0.0, 3.1.0, 3.1.1, 3.1.2, 3.1.3, 3.1.4, 3.1.5, 3.1.6, 3.1.7, and 3.8.3 are deprecated.

In addition to using Anypoint Runtime Manager, to deploy applications to Anypoint Runtime Fabric, you can also deploy applications by using the Mule Maven plugin. To do so, you must meet certain prerequisites, and configure your Runtime Fabric deployment strategy in your project's `pom.xml` file.

If you want to deploy applications to Runtime Fabric using a different method, see:

- Deploy Applications to Runtime Fabric Using Runtime Manager

### Prerequisites

- Ensure that the Mule Maven Plugin is added to your project
See Add the Mule Maven Plugin to a Mule Project for instructions.
- You understand and have available the number of resources required to deploy to Runtime Fabric +
See runtime fabric::deploy resource allocation self managedfor more information.
- The application is already published in Exchange +
See Publish and Deploy Exchange Assets Using Maven.

### Configure the Runtime Fabric Deployment Strategy

Inside the `plugin` element, add a configuration for your Runtime Fabric deployment, replacing the following placeholder values with your Runtime Fabric information:

```xml
<plugin>
[source,xml]
```

<groupId>org.mule.tools.maven</groupId>
  <artifactId>mule-maven-plugin</artifactId>
  <version>3.7.1</version>
  <extensions>true</extensions>
```text
  <configuration>
    <runtimeFabricDeployment>
      <uri>https://anypoint.mulesoft.com</uri>
      <muleVersion>4.3.0</muleVersion>
      <username>user</username>
      <password>pass</password>
      <applicationName>newapp</applicationName>
      <target>rtf</target>
      <environment>Sandbox</environment>
      <provider>MC</provider>
      <replicas>1</replicas>
      <properties>
        <key>value</key>
      </properties>
      <deploymentSettings>
        <enforceDeployingReplicasAcrossNodes>false</enforceDeployingReplicasAcrossNodes>
        <updateStrategy>recreate</updateStrategy>
        <clustered>false</clustered>
        <forwardSslSession>false</forwardSslSession>
        <lastMileSecurity>false</lastMileSecurity>
        <resources>
          <cpu>
            <reserved>20m</reserved>
            <limit>1500m</limit>
          </cpu>
          <memory>
            <reserved>700Mi</reserved>
          </memory>
        </resources>
        <http>
          <inbound>
            <publicUrl>url</publicUrl>
          </inbound>
        </http>
      </deploymentSettings>
    </runtimeFabricDeployment>
  </configuration>
</plugin>
```

### Deploy to Runtime Fabric

From the command line in your project's folder, package the application and execute the deploy goal:

```sh
mvn clean deploy -DmuleDeploy
```

#### Exchange Snapshot Assets

You can also deploy Exchange snapshot assets into Runtime Fabric.

By using `SNAPSHOT` version assets in Anypoint Exchange during the development and testing phase, you can avoid incrementing your application's version number for small changes. After your `SNAPSHOT` version application has been overwritten in Anypoint Exchange, you can redeploy your `SNAPSHOT` version application to Runtime Fabric via the Mule Maven plugin to deploy the latest changes.

To learn more about publishing snapshot assets to Anypoint Exchange, see Asset Lifecycle State.

Each time you update your application's snapshot, redeploy the application to refresh it with the latest snapshot binaries.

Because snapshot assets can change after deployment, avoid deploying them into your production environment.

### Redeploy to Runtime Fabric

To redeploy the application, run the same command as you did to deploy. +
Runtime Fabric rewrites the application you had deployed.

### Authentication Methods

When you deploy applications using Mule Maven plugin, you can use different methods to provide your credentials to authenticate against the deployment platform. Depending on the authentication method you use, the parameters to set in the deployment configuration differ:

| Authentication Method | Description | Configuration Parameters // tag::authenticationCloudHub[] |
|---|---|---|
| Username and password \| Use a CloudHub username and password to authenticate. \|* `username` + · `password` // end::authenticationCloudHub[] // tag::authenticationRTF[] | Username and password \| Use a Runtime Fabric username and password to authenticate. \|* `username` + · `password` // end::authenticationRTF[] // tag::authenticationOnPrem[] | Username and password \| Authenticate with the username and password for the server where your Mule instances are installed. \|* `username` + · `password` // end::authenticationOnPrem[] |
| Server \| Use credentials stored in a Maven server, configured inside the Maven `settings.xml` file. \| * `server` | Authorization Token \| Use an authorization token to access the platform. + See Identity Management for a list of supported single sign-on (SSO) types. \|* `authToken` | Connected Apps \|Use a Connected App to perform the authentication programmatically by communicating with Anypoint Platform. + Note that the Connected App credentials must have the `Design Center Developer` access scope. + See Connected Apps for Developers for instructions about creating Connected Apps. \|* `connectedAppClientId` + · `connectedAppClientSecret` + · `connectedAppGrantType` |

For a detailed description of the configuration parameters, see the Runtime Fabric Deployment Parameters Reference.

### Runtime Fabric Deployment Parameters Reference

| Parameter | Description | Required |
|---|---|---|
| `runtimeFabricDeployment` | Top-Level Element | Yes |
| `uri` | Your Anypoint Platform URI. + If not set, defaults to +https://anypoint.mulesoft.com+. \| No | `muleVersion` |
| The Mule runtime engine version to run in your Runtime Fabric instance.  + Ensure that this value is equal to or higher than the earliest required Mule version of your application.  By default, the latest available Mule version is selected. + Example values: `4.6.0` selects the last build where it defaults to Edge channel and Java 8. If you want to choose a different LTS or Edge selection or Java version, specify the full Mule version name as in `4.6.0:1e-java17`. + When using Mule Maven plugin versions 3.8.0 and 4.0.0 for deployments, the `muleVersion` property doesn't allow you to specify `releaseChannel` and `javaVersion`. To specify these properties, upgrade the plugin to version 4.1.1 or later. \| No | `releaseChannel` | Set the name of the release channel used to select the Mule image. Supported values are `NONE`, `EDGE`, and `LTS`. By default, the value is set to `EDGE`. If the selected release channel doesn't exist, an error occurs. |
| No | `javaVersion` | Set the Java version used in the deploy. Supported values are `8` and `17`. By default, the value is set to `8`. If the selected Java version doesn't exist, an error occurs. |
| No | `username` | Your Anypoint Platform username |
| Only when using Anypoint Platform credentials to login. | `password` | Your Anypoint Platform password |
| Only when using Anypoint Platform credentials to login. | `applicationName` | The application name displayed in Runtime Manager after the app deploys. |
| Yes | `target` | The Runtime Fabric target name where to deploy the app. |
| Yes | `provider` | Provider MC (MuleSoft Control Plane) indicates that the deployment is managed through Anypoint Runtime Manager. Set to `MC` for Runtime Fabric. |
| Yes | `environment` | Target Anypoint Platform environment. + This value must match an environment configured in your Anypoint Platform account, as shown here: + [source,xml,linenums] ---- <environment>Sandbox</environment> ---- |
| Yes | `replicas` | Specifies the number of replicas, or instances, of the Mule application to deploy. The maximum number of replicas per application is 16. |
| Only when `autoscaling` is set to `false`. | `businessGroup` | The Business group path of the deployment + Specify the full hierarchical path from the parent organization to the target Business group, for example: [source,xml,linenums] ---- <businessGroup>ParentOrg\SubOrg1\myBusinessGroup</businessGroup> ---- This value is omitted if `businessGroupId` is set. If `businessGroup` and `businessGroupId` are not set, the value defaults to the main business group of the user. |
| No | `businessGroupId` | The Business group ID of the deployment + Instead of specifying the Business group path, you can specify the Business group ID to deploy your application. If `businessGroupId` and `businessGroup` are not set, the value defaults to the main business group of the user. + The Business group ID is a mandatory parameter when you have access only to a specific Business group but not to the parent organization. + This parameter is available in plugin version 3.2.7 and later. \| No |
| `deploymentTimeout` | The allowed elapsed time, in milliseconds, between the start of the deployment process and the confirmation that the artifact has been deployed The default value is `600000`. \| No | `server` |
| Maven server with Anypoint Platform credentials + This is only needed if you want to use your credentials stored in your Maven `settings.xml` file. This is not the Mule server name. \| No | `properties` | Top-Level element + If you need to set properties for the Mule application you are deploying, you can use the `<properties>` top-level element: [source,xml,linenums] ---- <properties> <key>value</key> </properties> ---- For example: [source,xml,linenums] ---- <properties> <http.port>8081</http.port> </properties> ---- |
| No | `propertiesFile` | Top-level element + Specifies a file that contains properties for the Mule application being deployed. Use this parameter as an alternative to defining properties inline with `<properties>`. The file must use the Java properties format, with one `key=value` pair per line. \| No |
| `secureProperties` | Top-Level element + Use the `secureProperties` top-level element to set properties for the Mule application and instruct Runtime Fabric to encrypt the values before storing them: [source,xml,linenums] ---- <secureProperties> <key>value</key> </secureProperties> ---- For example: [source,xml,linenums] ---- <secureProperties> <http.port>8081</http.port> </secureProperties> ---- | No |
| `skip` | When set to `true`, skips the plugin deployment goal. + Its default value is `false`. \| No | `skipDeploymentVerification` |
| When set to `true`, skips the status verification of your deployed app. + Its default value is `false`. \| No | `authToken` | Specifies the authorization token to access the platform. You can use this authentication method instead of setting username and password. + See Identity Management for a list of supported single sign-on (SSO) types. \| Only when using an Authorization token to login. |
| `connectedAppClientId` | Specifies the Connected App `clientID` value. | Only when using Connected Apps credentials to login. |
| `connectedAppClientSecret` | Specifies the Connected App secret key. | Only when using Connected Apps credentials to login. |
| `connectedAppGrantType` | Specifies the only supported connection type: `client_credentials`. | Only when using Connected Apps credentials to login. |
| `deploymentSettings` | Any of the parameters documented in deploymentSettings Reference | No |

#### deploymentSettings Parameters Reference

| Parameter | Description |
|---|---|
| `enforceDeployingReplicasAcrossNodes` | Enforces the deployment of replicas across different nodes. The default value is `false`. Configuration example: [source,xml,linenums] ---- <deploymentSettings> <enforceDeployingReplicasAcrossNodes>false</enforceDeployingReplicasAcrossNodes> </deploymentSettings> ---- |
| `updateStrategy` |  [cols="1,3"] !=== ! Accepted values ! Description ! `rolling` ! Maintains availability by updating replicas incrementally. Requires one additional replica’s worth of resources to succeed. + If `enforceDeployingReplicasAcrossNodes` is enabled, the maximum number of replicas you can configure is one less than the total number of nodes. ! `recreate` ! Terminates replicas before re-deployment. Re-deployment is quicker than `rolling` and doesn’t require additional resources. + If `enforceDeployingReplicasAcrossNodes` is enabled, the maximum number of replicas you can configure is equal to the number of nodes. !=== The default value is `rolling`. Configuration example: [source,xml,linenums] ---- <deploymentSettings> <updateStrategy>recreate</updateStrategy> </deploymentSettings> ---- |
| `clustered` | Enables clustering across two or more replicas of the application. The default value is `false`. + Configuration example: [source,xml,linenums] ---- <deploymentSettings> <clustered>true</clustered> </deploymentSettings> ---- |
| `resources` |  [cols="1,1,3"] !=== .2+! `cpu` ! `reserved` ! Specifies the number of cores to allocate for each application replica. The default value is 0.5 vCores. ! `limit` ! Specifies the number of max cores to allocate for each replica of the application. + If a `reserved` configuration is present, ensure that this value is equal or higher. .2+! `memory` ! `reserved` ! Specifies the amount of memory to allocate for each application replica. The default value is 700 MB. ! `limit` ! Specifies the maximum memory allocated per application replica. If a `reserved` configuration is present, ensure that this value is equal or higher. !=== Configuration example: [source,xml,linenums] ---- <deploymentSettings> <resources> <cpu> <reserved>20m</reserved> <limit>1500m</limit> </cpu> <memory> <reserved>700Mi</reserved> </memory> </resources> </deploymentSettings> ---- |
| `http` |  [cols="1,1,3"] !=== .2+! `inbound` ! `publicUrl` ! URL of the deployed application. !=== Configuration example using wildcard URL: [source,xml,linenums] ---- <deploymentSettings> <http> <inbound> <publicUrl>https://myapp.example.com</publicUrl> </inbound> </http> </deploymentSettings> ---- Configuration example for path-based routing: [source,xml,linenums] ---- <deploymentSettings> <http> <inbound> <publicUrl>https://www.example.com/myapp</publicUrl> </inbound> </http> </deploymentSettings> ---- |
| `persistentObjectStore` | Configures the Mule application to use a persistent object store. By default, it is set to `false`. |
| `jvm` |  [cols="1,3"] !=== ! `args` ! Specifies JVM arguments to pass to Runtime Fabric when deploying the application. Use spaces to separate each argument. !=== Configuration example: [source,xml,linenums] ---- <deploymentSettings> <jvm> <args> -XX:MaxMetaspaceSize=500m -XX:MaxRAMPercentage=60.0 </args> </jvm> </deploymentSettings> ---- |
| `generateDefaultPublicUrl` | Not applicable for Runtime Fabric BYOK. By default, it is set to `false` |
| `disableAmLogForwarding` | Disables the application-level log forwarding to Anypoint Monitoring. By default, it is set to `false`. |
| `autoscaling` | Provides CPU based horizontal autoscaling configuration for deployment and redeployment operations. If autoscaling is disabled and the fields `minReplicas` and `maxReplicas` are provided, they must match the value of the `target.replicas` field. See Enable Trace Data Collection. Configuration example: [source,xml,linenums] ---- <deploymentSettings> <autoscaling> <enabled>true</enabled> <minReplicas>1</minReplicas> <maxReplicas>2</maxReplicas> </autoscaling> </deploymentSettings> ---- |

### Encrypt Credentials

To use encrypted credentials when deploying, you need to set up your Maven master encrypted password and your `settings-security.xml` file.

1. Create a master password for your Maven configuration.
```text
mvn --encrypt-master-password <yourMasterPassword>
```

Maven returns your master password encrypted:
```text
{l9vZ2uM5SdgHy+H12z4pX7LEOZn3Kbnqmt3kIquLjnQ=}
```

1. Create a `settings-security.xml` file in your ~/.m2 repository and add your encrypted master password:
```xml
<settingsSecurity>
  <master>{l9vZ2uM5SdgHy+H12z4pX7LEOZn3Kbnqmt3kIquLjnQ=}</master>
</settingsSecurity>
```

1. Encrypt your Anypoint platform password:
```text
mvn --encrypt-password <yourAnypointPlatformPassword>
```

Maven returns your Anypoint platform password encrypted:
```text
{HTWFGH5BG9QmvJ1B=}
```

1. Add your encrypted Anypoint Platform password to your `settings.xml` file in the <server> section:
```xml
<settings>
 ...
  <servers>
   ...
    <server>
      <id>my.anypoint.credentials</id>
      <username>my.anypoint.username</username>
      <password>{HTWFGH5BG9QmvJ1B=}</password>
    </server>
   ...
  </servers>
 ...
</settings>
```

1. In your configuration deployment, reference the credentials injecting the server ID configured in your `settings.xml` file:

```xml
<plugin>
  ...
  <configuration>
    ...
    <runtimeFabricDeployment>
      ...
      <server>my.anypoint.credentials</server>
      ...
    </runtimeFabricDeployment>
    ...
  </configuration>
  ...
<plugin>
```

> **Note:** Make sure that the username and password are not set in the deployment configuration, or they will overwrite the defined server ID.

## Deploy Applications to On-Premises Mule Instances Using the Mule Maven Plugin

Mule Maven plugin versions 3.0.0, 3.1.0, 3.1.1, 3.1.2, 3.1.3, 3.1.4, 3.1.5, 3.1.6, 3.1.7, and 3.8.3 are deprecated.

In addition to using Anypoint Studio, Anypoint Runtime Manager, or the Anypoint Platform CLI to deploy applications on-premises, you can also deploy Mule applications by using the Mule Maven plugin. To do so, you must meet certain prerequisites, and configure the desired deployment strategy in your project's `pom.xml` file.

If you want to deploy applications on-premises using a different method, see:

- Deploy Applications On-Premises Using Runtime Manager
- Deploy Applications On-Premises Using the Anypoint Platform CLI
- Deploy Applications On-Premises Using Anypoint Studio

### On-premises Deployment Strategies

When you deploy applications on-premises using the Mule Maven plugin, you can select three different methods for deployment:

- Standalone deployment +
By using this method you perform a manual deployment of your Mule application to your on-premises Mule instance.
- Runtime Manager REST API deployment +
This method enables you to deploy an application using the Runtime Manager REST API, which links your on-premises Mule instance with your Anypoint Runtime Manager account, where you can do further management and monitoring of your deployed application.
- Runtime Manager Agent deployment +
This method enables you to deploy an application using the Runtime Manager agent, which exposes a local API that you can call to manage and monitor your deployed application.

The Mule Maven plugin also supports deploying domains when using the standalone deployment strategy, or the Runtime Manager agent deployment strategy.

Additional operations enable you to deploy applications in parallel and update applications at runtime.

### Prerequisites

- Add the Mule Maven Plugin to your project
See Add the Mule Maven Plugin to a Mule Project for instructions.

### Deploy a Mule Application to a Standalone Mule Runtime Engine

Inside the `plugin` element, add a configuration for your standalone deployment, replacing the placeholder values with your local Mule runtime engine information:

```xml
<plugin>
[source,xml]
```

<groupId>org.mule.tools.maven</groupId>
  <artifactId>mule-maven-plugin</artifactId>
  <version>3.7.1</version>
  <extensions>true</extensions>
```text
  <configuration>
    <standaloneDeployment>
      <muleHome>${mule.home.test}</muleHome>
      <muleVersion>${app.runtime}</muleVersion>
    </standaloneDeployment>
  </configuration>
</plugin>
```

From the command line in your project's folder, package the application and execute the deploy goal:

```text
mvn clean deploy -DmuleDeploy
```

#### Standalone Deployment Parameters Reference

| Parameter | Description | Required |
|---|---|---|
| `standaloneDeployment` | Top-Level Element. | Yes |
| `applicationName` | Specifies the application name to use during deployment. | Yes |
| `muleVersion` | The Mule version running in your local machine instance. + If this value does not match the Mule version running in your deployment target, the plugin raises an exception. The Mule Maven Plugin does not download a Mule runtime engine if these values don't match. \| Yes | `muleHome` |
| The location of the Mule instance in your local machine. | Yes | `deploymentTimeout` |
| The allowed elapsed time, in milliseconds, between the start of the deployment process and the confirmation that the artifact has been deployed The default value is `600000`. \| No | `skip` | When set to `true`, skips the plugin deployment goal. + Its default value is `false`. \| No |

### Deploy a Mule Application Using the Runtime Manager REST API

Mule Maven plugin enables you to deploy a Mule Application to a local Mule instance using the Runtime Manager REST API.

#### Prerequisites

- You need a server, server group or cluster created in Runtime Manager. +
  - To create a server, see Add Servers. +
  - To create a server group, see Create Server Groups. +
  - To create a cluster, see Create Clusters. +

#### Deploying Using the Runtime Manager REST API

Inside the `plugin` element, add a configuration for your Runtime Manager deployment, replacing the placeholder values with your Runtime Manager information:

```xml
<plugin>
[source,xml]
```

<groupId>org.mule.tools.maven</groupId>
  <artifactId>mule-maven-plugin</artifactId>
  <version>3.7.1</version>
  <extensions>true</extensions>
```text
  <configuration>
    <armDeployment>
      <muleVersion>${app.runtime}</muleVersion>
      <uri>https://anypoint.mulesoft.com</uri>
      <target>${target}</target>
      <targetType>${target.type}</targetType>
      <username>${username}</username>
      <password>${password}</password>
      <environment>${environment}</environment>
      <properties>
        <key>value</key>
      </properties>
    </armDeployment>
  </configuration>
</plugin>
```

From the command line in your project's folder, package the application and execute the deploy goal:

```text
mvn clean deploy -DmuleDeploy
```

#### Authentication Methods

When you deploy applications using Mule Maven plugin, you can use different methods to provide your credentials to authenticate against the deployment platform. Depending on the authentication method you use, the parameters to set in the deployment configuration differ:

| Authentication Method | Description | Configuration Parameters // tag::authenticationCloudHub[] |
|---|---|---|
| Username and password \| Use a CloudHub username and password to authenticate. \|* `username` + · `password` // end::authenticationCloudHub[] // tag::authenticationRTF[] | Username and password \| Use a Runtime Fabric username and password to authenticate. \|* `username` + · `password` // end::authenticationRTF[] // tag::authenticationOnPrem[] | Username and password \| Authenticate with the username and password for the server where your Mule instances are installed. \|* `username` + · `password` // end::authenticationOnPrem[] |
| Server \| Use credentials stored in a Maven server, configured inside the Maven `settings.xml` file. \| * `server` | Authorization Token \| Use an authorization token to access the platform. + See Identity Management for a list of supported single sign-on (SSO) types. \|* `authToken` | Connected Apps \|Use a Connected App to perform the authentication programmatically by communicating with Anypoint Platform. + Note that the Connected App credentials must have the `Design Center Developer` access scope. + See Connected Apps for Developers for instructions about creating Connected Apps. \|* `connectedAppClientId` + · `connectedAppClientSecret` + · `connectedAppGrantType` |

For a detailed description of the configuration parameters, see the Runtime Manager REST API Deployment Parameters Reference.

#### Runtime Manager REST API Deployment Parameters Reference

| Parameter | Description | Required |
|---|---|---|
| `armDeployment` | Top-Level Element. | Yes |
| `applicationName` | Specifies the application name to use during deployment. | Yes |
| `muleVersion` | The Mule version required for your application to run in your deployment target. + If this value does not match the Mule version running in your deployment target, the plugin raises an exception. The Mule Maven Plugin does not download a Mule runtime engine if these values don't match. \| Yes | `uri` |
| The Anypoint Platform URI. If you are using Anypoint Platform PCE, specify this parameter with your Anypoint Platform installation URI. + If not set, by default this value is set to +https://anypoint.mulesoft.com+. \| No | `target` | The server name for the server where your Mule instances are installed. |
| Yes | `targetType` | The type of target to which you are deploying. Valid values are: · server · serverGroup · cluster |
| Yes | `username` | Your username for the server where your Mule instances are installed. |
| Only when using Anypoint Platform credentials to login. | `password` | Your password for the server where your Mule instances are installed. |
| Only when using Anypoint Platform credentials to login. | `environment` | The environment name for the server where your Mule instances are installed. This value must match any environment configured in your Runtime Manager account. + For Example: [source,xml,linenums] ---- <environment>Sandbox</environment> ---- |
| Yes | `businessGroup` | The Business group path of the deployment + Specify the full hierarchical path from the parent organization to the target Business group, for example: [source,xml,linenums] ---- <businessGroup>ParentOrg\SubOrg1\myBusinessGroup</businessGroup> ---- This value is omitted if `businessGroupId` is set. If `businessGroup` and `businessGroupId` are not set, the value defaults to the main business group of the user. |
| No | `businessGroupId` | The Business group ID of the deployment + Instead of specifying the Business group path, you can specify the Business group ID to deploy your application. If `businessGroupId` and `businessGroup` are not set, the value defaults to the main business group of the user. + The Business group ID is a mandatory parameter when you have access only to a specific Business group but not to the parent organization. + This parameter is available in plugin version 3.2.7 and later. \| No |
| `deploymentTimeout` | The allowed elapsed time, in milliseconds, between the start of the deployment process and the confirmation that the artifact has been deployed The default value is `600000`. \| No | `server` |
| Maven server with Anypoint Platform credentials + This is only needed if you want to use your credentials stored in your Maven `settings.xml` file. This is not the Mule server name. \| No | `properties` | Top-Level element + If you need to set properties for the Mule application you are deploying, you can use the `<properties>` top-level element: [source,xml,linenums] ---- <properties> <key>value</key> </properties> ---- For example: [source,xml,linenums] ---- <properties> <http.port>8081</http.port> </properties> ---- |
| No | `propertiesFile` | Top-level element + Specifies a file that contains properties for the Mule application being deployed. Use this parameter as an alternative to defining properties inline with `<properties>`. The file must use the Java properties format, with one `key=value` pair per line. \| No |
| `skip` | When set to `true`, skips the plugin deployment goal. + Its default value is `false`. \| No | `skipDeploymentVerification` |
| When set to `true`, skips the status verification of your deployed app. + Its default value is `false`. \| No | `authToken` | Specifies the authorization token to access the platform. You can use this authentication method instead of setting username and password. + See Identity Management for a list of supported single sign-on (SSO) types. \| Only when using an Authorization token to login. |
| `connectedAppClientId` | Specifies the Connected App `clientID` value. | Only when using Connected Apps credentials to login. |
| `connectedAppClientSecret` | Specifies the Connected App secret key. | Only when using Connected Apps credentials to login. |
| `connectedAppGrantType` | Specifies the only supported connection type: `client_credentials`. | Only when using Connected Apps credentials to login. |

#### Encrypt Credentials

To use encrypted credentials when deploying, you need to set up your Maven master encrypted password and your `settings-security.xml` file.

1. Create a master password for your Maven configuration.
```text
mvn --encrypt-master-password <yourMasterPassword>
```

Maven returns your master password encrypted:
```text
{l9vZ2uM5SdgHy+H12z4pX7LEOZn3Kbnqmt3kIquLjnQ=}
```

1. Create a `settings-security.xml` file in your ~/.m2 repository and add your encrypted master password:
```xml
<settingsSecurity>
  <master>{l9vZ2uM5SdgHy+H12z4pX7LEOZn3Kbnqmt3kIquLjnQ=}</master>
</settingsSecurity>
```

1. Encrypt your Anypoint platform password:
```text
mvn --encrypt-password <yourAnypointPlatformPassword>
```

Maven returns your Anypoint platform password encrypted:
```text
{HTWFGH5BG9QmvJ1B=}
```

1. Add your encrypted Anypoint Platform password to your `settings.xml` file in the <server> section:
```xml
<settings>
 ...
  <servers>
   ...
    <server>
      <id>my.anypoint.credentials</id>
      <username>my.anypoint.username</username>
      <password>{HTWFGH5BG9QmvJ1B=}</password>
    </server>
   ...
  </servers>
 ...
</settings>
```

1. In your configuration deployment, reference the credentials injecting the server ID configured in your `settings.xml` file:

```xml
<plugin>
  ...
  <configuration>
    ...
    <armDeployment>
      ...
      <server>my.anypoint.credentials</server>
      ...
    </armDeployment>
    ...
  </configuration>
  ...
<plugin>
```

> **Note:** Make sure that the username and password are not set in the deployment configuration, or they will overwrite the defined server ID.

#### Troubleshoot TLS Errors in Anypoint Private Cloud Edition

When trying to connect to an instance of Runtime Manager that's on an Anypoint Platform Private Cloud Edition installation, the plugin validates certificates for that server. If you haven't installed the server certificates in your truststore, an SSL error occurs. To avoid this problem, you can run the plugin in an insecure mode, which skips the security validations. You can use the **armInsecure** tag or the **arm.insecure** system property.

Enabling an insecure connection is a dangerous practice. Don't use this unless you know what you are doing and your On-Premises installation is isolated in a local network.

See the configuration example below:

```xml
<plugin>
[source,xml]
```

<groupId>org.mule.tools.maven</groupId>
  <artifactId>mule-maven-plugin</artifactId>
  <version>3.7.1</version>
  <extensions>true</extensions>
```text
  <configuration>
    <armDeployment>
        <target>${target}</target>
        <targetType>${target.type}</targetType>
        <username>${username}</username>
        <password>${password}</password>
        <environment>${environment}</environment>
        <armInsecure>true</armInsecure>
    </armDeployment>
  </configuration>
</plugin>
```

### Deploy a Mule Application Using the Runtime Manager Agent

Inside the `plugin` element, add a configuration for your Runtime Manager agent deployment, replacing the URI value with your remote server information:

```xml
<plugin>
[source,xml]
```

<groupId>org.mule.tools.maven</groupId>
  <artifactId>mule-maven-plugin</artifactId>
  <version>3.7.1</version>
  <extensions>true</extensions>
```text
  <configuration>
    <agentDeployment>
      <uri>http://localhost:9999/</uri>
    </agentDeployment>
  </configuration>
</plugin>
```

From the command line in your project's folder, package the application and execute the deploy goal:

```text
mvn clean deploy -DmuleDeploy
```

#### Runtime Manager Agent Deployment Parameters Reference

| Parameter | Description | Required |
|---|---|---|
| `agentDeployment` | Top-Level Element. | Yes |
| `applicationName` | Specifies the application name to use during deployment. | Yes |
| `muleVersion` | The Mule version required for your application to run in your deployment target. + If this value does not match the Mule version running in your deployment target, the plugin raises an exception. The Mule Maven Plugin does not download a Mule runtime engine if these values don't match. \| Yes | `uri` |
| The server URI where your Mule instances are installed. | Yes | `deploymentTimeout` |
| The allowed elapsed time, in milliseconds, between the start of the deployment process and the confirmation that the artifact has been deployed The default value is `600000`. \| No | `skip` | When set to `true`, skips the plugin deployment goal. + Its default value is `false`. \| No |

### Deploy a Domain

The Mule Maven plugin supports deploying domains only when using the standalone deployment strategy, or the Runtime Manager agent deployment strategy.

To deploy a domain, use the same configuration and deployment steps you use when deploying an application. For example, to deploy a domain to a standalone instance:

1. Inside the `plugin` element, add a configuration for your standalone deployment, replacing the placeholder values with your local Mule runtime engine information:
```xml
<plugin>
[source,xml]
```

<groupId>org.mule.tools.maven</groupId>
  <artifactId>mule-maven-plugin</artifactId>
  <version>3.7.1</version>
  <extensions>true</extensions>
```text
  <configuration>
    <standaloneDeployment>
      <muleHome>${mule.home.test}</muleHome>
      <muleVersion>${app.runtime}</muleVersion>
    </standaloneDeployment>
  </configuration>
</plugin>
```

1. From the command line in your project's folder, package the domain and execute the deploy goal:
```text
mvn clean deploy -DmuleDeploy
```

### Deploy Applications in Parallel

You can deploy applications in parallel to on-premises Mule instances. Deploying applications in parallel reduces the startup time when you deploy a large number of apps. To prevent deployment failure, ensure that applications are not dependent on each other because a particular start order cannot be guaranteed.

Parallelism is fixed at 20.

To enable parallel deployment:

1. Package or export your Mule applications to the `/apps` directory of your Mule runtime engine instance.
1. Start Mule using the `-M-Dmule.deployment.parallel` option:
```
mule -M-Dmule.deployment.parallel
```

After performing these steps, Mule deploys in parallel all applications in the `/apps` directory.

### Undeploy Applications

You can undeploy Mule applications by deleting an app's anchor file only instead of deleting the application folder directly.

Deleting only the app’s anchor file:

- Prevents any interference from the hot-deployment layer and leaves no room for concurrent conflicting actions.

- Avoids potential application JAR file locking issues on some operation systems and allows for clean shutdown and undeployment.

For example, if the `stockTrader` app is running (app folder is there as well as the `$MULE_HOME/apps/stockTrader-anchor.txt` file), just delete the anchor file to have the app removed from the Mule instance at runtime. Application folder is removed after the app terminates.

After undeploying a Mule application, there is a timeout of 15 seconds until `LoggerContext` stops. Log files for an application only release after this timeout expires. This information is important in Windows, where you can’t remove files that are in use by other processes.
After undeploying a Mule application, there is a timeout of 15 seconds until LoggerContext stops. Log files for an application only release after this timeout expires. This information is important in Windows, where you can’t remove files that are in use by other processes.

### Update Applications at Runtime

Updating a Mule application at runtime can be a complex change involving class modifications, endpoint modifications (for example, changing ports), and reconfiguring flows. An application update first performs a graceful app shutdown and then reconfigures itself in the background within seconds. This process is transparent for the users.

There are two ways you can update an application:

- By adding the modifications over an existing unpacked app folder and touching the main configuration file (`mule-config.xml` located in the app's root directory by default). +
For this option to be valid, start the runtime with the system property `-M-Dmule.deployment.forceParseConfigXmls=true`.
- By adding a new `jar` with an updated version of the app into the `$MULE_HOME/apps` directory. Mule detects the `jar` as an updated version of an existing application and ensures the update by a clean redeployment of the app. +
Note that Mule discards any modifications to the old application folder. The new app folder is a clean unpacked application from a `jar`.

Either method integrates well with existing build tools.

## Configuring Environment Properties

You can configure your Mule application to automatically load property files based on the development environment (QA, preproduction, production, etc) you are working on, making it easier to deploy your app both on-premises and in the cloud. This configuration requires you to complete the following tasks:

1. Create a properties file for each development environment in your application.

1. Configure a properties placeholder in your app to look for the environment upon launch.

1. Set an environment variable to point to a specific development environment during application deployment.

Consider externalizing other aspects of your configuration, like time-out values, polling frequencies, and so on, even if these configurations don't vary between environments. This configuration facilitates tuning and experimenting because the Mule application becomes fully configurable through a single properties file.

Download Example Studio Application

### Considerations when Using Environment Properties

Consider the following guidelines when you configure environment properties:

- Use a consistent naming strategy for your properties files and make them unique across applications.
This practice ensures that files are easy to reuse across teams. A good strategy is to add the application name or application ID to the properties file names.
- If you are deploying multiple applications through a shared resources structure, do not set anything in the properties files.
Doing so can cause conflicts between the various apps that share a domain. Instead, you can set environment variables that span the scope of the deployed app, its domain, and other apps under that domain.
In Studio, you can create environment variables using the **Environment** tab of the **Run Configurations** menu. You can access the Environment tab from the drop-down menu to the right of the **Play** button.

### Basic Architecture of an Environment Property Configuration

The following Mule configuration fragment defines a global property called `env`, a dynamic configuration properties file (based on the `env` property), and an HTTP connector with variable configuration:

```xml

<global-property doc:name="Global Property" name="env" value="qa" />
<configuration-properties doc:name="Configuration properties" file="${env}.yaml" />
<http:listener-config name="HttpListenerConfiguration"
                      doc:name="HTTP Listener Configuration"
                      host="${host}"
                      port="${port}"
                      basePath="${path}" />
```

This example uses Spring's property placeholder resolution mechanism. The variable bits: the **base path**, **host**, and **port** are clearly visible and can vary for each environment where this connector gets deployed in.

When deploying your application, you can dynamically replace the `env` property with the particular environment to which you're deploying, such as `qa` or `prod`. This causes the Mule application to load a different `.yaml` file with properties specific to the configured environment.

To provide values for these environment variables, we use a Yaml configuration file for each environment:

**Properties File: qa.yaml**

```text
path: "test/products"
host: "localhost"
port: 8082
```

**Properties File: prod.yaml**

```text
path: "products"
host: "www.acme.com"
port: 8081
```

### Creating and Configuring Environment Properties

Create variable properties files and configure them in your application to look for the environment upon launch. Additionally, you can test environment properties in Studio. To complete these tasks review the following steps:

#### Using Studio Visual Editor

1. Define a list of environments you wish to support in your application. For example, one common use case involves configuring the application to support both Production and a QA environments. +
We will define the variable `variable` in the environments `prod` and `qa` and test it using a single application.

1. Right-click the `src/main/resources` folder, then select  **New**  >  **File**   to create a properties file for each environment you wish to support. For example:
  - `qa.yaml`
  - `prod.yaml`

1. Double-click each of these new files to open them in new tabs in Studio. By editing them, you can configure the properties of the environment that correspond to the filename. For example, you may wish to add the properties as per the following images. Keep in mind that you can use these properties anywhere in your application.

1. Close the properties files.

1. Click in the Global Elements tab of your Studio project, below the canvas.

1. **Create** a new global element.  When selecting the element type, pick **Configuration properties**  under **Global Configurations**.

1. Set the value of the **File** field to `+++$+++.yaml`
1. **Create** a new property to add a default environment. When selecting the element type, pick **Global Property**  under **Global Configurations**.

1. Set a value to the property.

1. You can change the environment by editing the configured **Global Property** value.

#### Using XML Editor

1. Define a list of environments you wish to support in your application. For example, one common use case involves configuring the application to support both Production and a QA environments. +
We will define the variable `variable` in the environments `prod` and `qa` and test it using a single application.

1. Right-click the  `src/main/resources`  folder, then select  **New**  >  **File**   to create a properties file for each environment you wish to support. For example:
  - `qa.yaml`
  - `prod.yaml`

1. Double-click each of these new files to open them in new tabs in Studio. By editing them, you can configure the properties of the environment that correspond to the filename. For example, you may wish to add the properties as per the following images. Keep in mind that you can use these properties anywhere in your application.

1. Close the properties files.

1. Click in the Configuration XML tab of your Studio application, below the canvas.

1. Add a **configuration-properties** element to the XML file and let the file name configurable.

```xml
<configuration-properties doc:name="Configuration properties" file="${env}.yaml" />
```

1. Add a **Global Property** element to set the default environment name.

```xml
<global-property doc:name="Global Property" name="env" value="qa" />
```

1. You can change the environment by editing the configured **Global Property** value.

#### Testing Configured Environment Properties in Studio

You can test that your application uses the specific environment you configured in your variables properties file, by running the application in Mule embedded in Studio.

1. In the Package Explorer view, right-click the filename of the project you wish to deploy, then select **Run As** > **Mule Application**.

1. Studio automatically deploys your application according to the environment variable you specified in the **Global Property** from the previous procedure.

1. Again in the Package Explorer view, right-click the filename of the project you wish to deploy, then select **Run As** > **Run Configurations...**.

1. Define the System Property in the `Arguments` tab.

1. Click the `Run` button to complete the procedure. The properties configured in `prod.yaml` will be used instead of the ones defined in `qa.yaml`.

### Setting Environment Variables for Application Deployment

Mule loads the environment variables when it starts, so depending on your deployment target (CloudHub or On-premises) you need to set the environment when you deploy the app (CloudHub) or when you start your Mule instance (On-premises).

#### Setting a Specific Environment when Starting Mule On-Premises

##### Using the command line

Identify the environment in which to deploy your application at runtime with an environment variable. Execute the command to run Mule in your environment as per the following example:

```text
$ mule -M-Denv=prod
```

Once Mule starts with your configured environment, you can deploy the application with your desired deployment method.

##### Using Anypoint Runtime Manager

As a prerequisite you need to create a server in Anypoint Runtime Manager and link it to Mule. Then you can create a custom server property.

#### Setting a Specific Environment when Deploying to CloudHub

##### Deploying to CloudHub from Studio

From Studio you can initiate the process to set your properties environment variables and deploy your application to CloudHub :

1. In the Package Explorer view, right-click the filename of the project you wish to deploy, then select **Anypoint Platform** -> **Deploy to Cloud**.

1. Complete the requested data, and click the **Properties** tab.

1. Add a new environment variable by setting **Key** to **env** and its value to **prod**.

1. Click **Deploy Application**.

##### Deploying to CloudHub from Runtime Manager

To deploy your application to CloudHub via Anypoint Runtime Manager, you can set properties values using Runtime Manager Console.

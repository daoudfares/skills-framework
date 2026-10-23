# Anypoint Code Builder: local workflow

> Derived from the Anypoint Code Builder documentation at docs.mulesoft.com.

## Anypoint Code Builder Overview

Use Anypoint Code Builder for your API designs, implementations, and integration development. Work
locally with Anypoint Code Builder on Microsoft Visual Studio Code (VS Code). Anypoint Code Builder
supports the development lifecycle:

- API specification design, a mocking service for testing, source control, and publication to
  Anypoint Exchange

- API implementation features for importing supported API specifications (such as OAS, RAML,
  AsyncAPI, or GraphQL) and autogenerating interfaces (scaffolding) for flows and error handlers
  within a Mule application

- Integration development to connect systems, transform data to required formats, and provide
  business logic to manage messages and events programmatically within a Mule application

You can share project snapshots with members of your team by using import and export features or by
using a source control management (SCM) system of your choice.

For an introduction to Anypoint Code Builder, see our Trailhead badge,
[Anypoint Code Builder: Quick Look](https://trailhead.salesforce.com/content/learn/modules/mulesoft-anypoint-code-builder-quick-look)
(login required). Sign up if you don’t have a Trailhead account.

### Anypoint Extension Pack

Get the Anypoint Code Builder experience through the Anypoint Extension Pack for Visual Studio Code.
The extensions require installation to VS Code. See
Getting Started with Anypoint Code Builder.

### Cloud Hosts

Anypoint Code Builder is available through Anypoint Platform from US, EU, Canada, Japan, India, and
Australia cloud hosts. To help your organization meet emerging regulatory requirements that differ
by region, Anypoint Platform does not share organization information, permissions, account data, or
projects between hosts.

| Control Plane | Platform URL | Description |
|---|---|---|
| US Cloud | anypoint.mulesoft.com | Non-EU region host. MuleSoft hosts this control plane within data centers in the United States. |
| EU Cloud | eu1.anypoint.mulesoft.com | EU-compliant host. MuleSoft hosts this control plane within EU (Frankfurt) data centers. |
| Canada Cloud | ca1.platform.mulesoft.com | MuleSoft hosts this control plane within Canada (North America) data centers. |
| Japan Cloud | jp1.platform.mulesoft.com | MuleSoft hosts this control plane within Japan (APAC) data centers. |
| India Cloud | in1.platform.mulesoft.com | MuleSoft hosts this control plane within India (APAC) data centers. |
| Australia Cloud | au1.platform.mulesoft.com | MuleSoft hosts this control plane within Australia (APAC) data centers. |

Anypoint Platform hosts deployment targets for managed Mule runtime versions and related data,
including data and metadata about your Mule implementations.

To change the host from the default (US), see
Set Anypoint Code Builder to a Different Control Plane.

Use of Anypoint Code Builder requires an Anypoint Platform user account. Use of some features
requires permissions set by an organization administrator (see
Configuring Permissions).

If you do not have an Anypoint Platform account through your organization, you can sign up in the US
or EU cloud host for Anypoint Platform.

See Anypoint Platform Hosting Overview for more information.

### Get Familiar with the Basics

Some knowledge about designing an API using API specification languages (such as OAS, RAML,
AsyncAPI, or gRPC) can be helpful. API implementations and integration development require
familiarity with Mule application development, connectors, and the DataWeave transformation
language. Anypoint Code Builder Tutorials help you get started with these tasks.

It’s also useful to be familiar with these products and features:

- Anypoint Connectors provide operations for retrieving, modifying, and sending data to and from
  systems. Anypoint Code Builder provides built-in connectors
  and access to many other connectors from Anypoint Exchange.

- Core processors (also called Core components or Mule components) are programmatic building blocks
  that provide the business logic for integration and implementation applications. Examples include
  For Each (`<foreach/>`), Transform Message (`<ee:transform/>`), and Flow (`<flow/>`). See
  Anypoint Code Builder Components and Commands Reference.

- DataWeave is the programming language for all expressions and data transformations in your
  integrations and implementations. The language offers function libraries and mechanisms for
  creating customizations, including your own functions, libraries, and data types. To learn the
  basics of DataWeave and experiment with DataWeave scripts, see
  [DataWeave Tutorial and Playground](https://dataweave.mulesoft.com/).

- Scaffolding is an automatic process that uses APIkit to take an API specification as input and
  autogenerate an XML-based router and endpoints that you implement within a Mule application.

- A flow is a block of components, including any connector operations, that Mule runtime engine
  (Mule) executes sequentially on an event and the message it contains. A flow can also contain an
  operation that triggers the creation of the event and initiates the execution of the flow.

  A subflow is similar to a flow but does not support the configuration of triggers (sometimes
  called message sources), which are exclusive to flows.

  A flow reference enables you to trigger execution of a flow or subflow from another flow.

- A Mule application contains one or more XML-based configuration files for your connectors,
  components, secure configuration properties, scaffolded API specifications, and other parts of
  your integrations and implementations. The application runs on Mule and is part of a project that
  contains the resources needed to configure, build, run, test, and deploy the application.

- Business groups organize APIs, Mule applications, and other resources within an Anypoint Platform
  organization. Organization administrators create and control access to business groups. For
  details about business groups, organizations, and related management features, see
  Anypoint Platform Business Groups.

### Anypoint Platform Product Integrations

Anypoint Code Builder integrates with key Anypoint Platform products and features:

- Anypoint Exchange for publishing the API specifications that you create and importing API
  specifications and development resources (such as connectors, integration project templates and
  examples) into your projects

- CloudHub and CloudHub 2.0 for deploying the implementations and integrations that you build

- MuleSoft VCS for importing API specification projects into Anypoint Code Builder and optionally,
  synchronizing imported projects by using the Anypoint source control management (SCM) system

The use of features provided by Anypoint Platform products requires a connection. You establish this
connection by logging in to your Anypoint Platform account from Anypoint Code Builder. For more
information, see Sign in to Anypoint Platform from Anypoint Code Builder.

### Source and Version Control

Use any supported source control management (SCM) system. VS Code supports Git out-of-the-box in
addition to several extensions for popular version control and SCM systems.

For guidance with Git setup in Anypoint Code Builder, see Controlling Source Files.

See VS Code documentation on
[Git support](https://code.visualstudio.com/docs/sourcecontrol/overview) and
[extensions for other SCM providers](https://code.visualstudio.com/docs/sourcecontrol/overview#_scm-providers).
For extension authors only, VS Code also provides a
[VS Code source control API](https://code.visualstudio.com/api/extension-guides/scm-provider).

### Anypoint Code Builder Startup

Anypoint Code Builder optimizes Maven bookkeeping and bundle-loading operations during
initialization. This behavior reduces startup overhead so workspaces can become available with less
wait time.

It also reads extension bundle directories directly from the extension path when loading workspace
assets. This initialization path reduces delays before projects are ready for development tasks.

### Feedback

To provide feedback about Anypoint Code Builder, complete the
[feedback survey](https://www.surveymonkey.com/r/acb_feedback).

For questions or general discussion about Anypoint Code Builder, see
[Trailblazer Discussion Topic](https://trailhead.salesforce.com/trailblazer-community/topics/mulesoftanypointcodebuilder?sort=LAST_MODIFIED_DATE_DESC).

## Version Settings for Mule, Java, and Connectors

Set Mule runtime engine (Mule), Java, and connector versions to use in your projects.

Anypoint Code Builder includes bundled Mule runtime versions so you can open and design projects
instantly without additional Mule runtime downloads. Anypoint Code Builder uses these bundled Mule
runtime versions for editing and DataSense. Exact Mule runtime versions are only required when you
run or debug your applications.

- Bundled runtimes: Learn about the Mule runtime versions included with
  Anypoint Code Builder.

- Default versions: Set default Mule and Java versions to show in version
  dropdown menus.

- Project-level versions: Set versions to use in a specific project.

  - For Mule and Java versions, see
    Select Mule and Java Versions for a Project.

  - For connector versions, see
    Select Connector Versions for a Project.

- Install additional runtimes: Download specific Mule runtime
  versions when needed for run or debug operations.

### Bundled Mule Runtime Versions

Anypoint Code Builder includes two bundled Mule runtime versions that are available immediately
after installation:

- **Mule 4.8 (Java 8 compatible)**: A minimal Mule runtime version bundle compatible with all Java
  8-based Mule 4.4 and later projects. This Mule runtime version is used for design-time activities
  with Java 8 projects and serves as the default fallback for legacy applications. You can’t use
  this version to run Mule applications.

- **Latest Runtime (Java 17)**: The most recent supported Mule runtime version (Edge or LTS) bundled
  with Anypoint Code Builder at the time of release. For example, Mule 4.12.0. This Mule runtime
  version supports Java 17 and can be used for both designing and running applications. Projects
  configured for Mule 4.6, 4.9, 4.10, and 4.11 are compatible with this bundled Mule runtime
  version.

Anypoint Code Builder automatically selects the appropriate bundled Mule runtime version based on
your project’s Java version:

- Java 8 projects use the bundled 4.8 minimal Mule runtime version

- Java 17 projects use the latest bundled Mule runtime version

These bundled Mule runtime versions guarantee that the design service can always start and serve the
canvas and design-time needs without requiring Mule runtime downloads. Projects open instantly using
these bundled Mule runtime versions. Download a specific Mule runtime version if you want to run or
debug your application with an exact version that isn’t available locally.

### Select Default Mule and Java Versions

Select the default Mule and Java versions for new implementation and integration projects. The
defaults appear in drop-down menus from which you select a version, for example, when creating a
project.

The dropdown shows only locally available Mule runtime versions, including the bundled ones.
Versions that don’t support a feature typically append a message, such as **AsyncAPI implementation
unsupported** for Mule 4.4.

You can set a different version at the project level (see
Select Mule and Java Versions for a Project).

To select the default Mule and Java versions from the **Settings** tab:

2.  Find **Mule › Application: Default Mule Runtime And Java Versions** in the open tab.

### Select Mule and Java Versions for a Project

Set Mule or Java versions for a specific implementation or integration project from **Project
Properties**. You can change versions at any time, but test your projects with the versions you
intend to deploy.

Anypoint Code Builder uses bundled Mule runtime versions to open and edit projects immediately. The
design service uses the latest Java-compatible Mule runtime version available locally. Anypoint Code
Builder bundles the latest Mule runtime version (for example, 4.12) for Java 17 and a reduced Mule
runtime version 4.8 for Java 8. This guarantees that the design service can always start and serve
the canvas and design-time needs without requiring Mule runtime downloads.

Because the bundled Mule runtime version is the latest one, you can open and edit any project
regardless of its `minMuleVersion` property. The design service uses the latest Java-compatible Mule
runtime version available locally for design-time activities. The `minMuleVersion` property in your
project’s `mule-artifact.json` file is checked only at deployment time. The `minMuleVersion`
property specifies the minimum Mule runtime version required to run or deploy the application.

Version settings are important in several scenarios:

- Updating a project to use more current versions

- Switching to a supported version, for example, for a project that you import into Anypoint Code
  Builder that uses an unsupported version

- Selecting versions of Mule or Java that are compatible with each other

- Specifying exact Mule runtime versions for run and debug operations

When you run or debug an application, Anypoint Code Builder checks if the exact Mule runtime version
specified in your project is available locally. If not, you see a warning dialog that allows you to:

- Continue with the latest compatible local version

- Open **Project Properties** to select or download the required Mule runtime version

> [!NOTE] Changing the minimum Mule version (`minMuleVersion`) manually can have serious
> implications. This requires a full test of your application so it works correctly with the target
> Mule runtime version. Newer Mule runtime versions turn on feature flags by default. See
> Feature Flagging Mechanism. This can change behavior
> that was fixed in later versions. Your application can rely on behavior that was later corrected
> or on a previous issue. Prefer changing the Mule runtime version through **Project Properties**,
> and always run full regression tests after any version change.

When a Mule or Java version isn’t set for a project, the canvas and notifications provide a **Set
version** button that opens the **Project Properties** tab. You can also navigate directly to the
**Project Properties** tab.

To select Mule and Java versions for a project:

1.  Open your implementation or integration project

2.  Run this command to open the **Project Properties** tab:

    ```command
    MuleSoft: Open Mule Project Properties
    ```

4.  In **Project Properties**, select the versions to use in this project.

    You can select from locally available Mule runtime and Java versions. The dropdown shows only
    the Mule runtime versions that are installed on your local disk, including bundled Mule runtime
    versions that are available immediately after installation. Anypoint Code Builder saves your
    version settings to the project’s `mule-artifact.json` file. Bundled Mule runtime versions
    enable instant project opening and design. To install additional Mule runtime versions, use the
    `MuleSoft: Install Runtime` command. For information about version support and automated Mule
    patch updates, see Mule and Java version support.

### Select Connector Versions for a Project

Set connector versions for a specific implementation or integration project from **Project
Properties** or when you add a component to the canvas. You can change versions at any time, but it
is important to test your projects with the versions you intend to deploy.

To select connector versions for a project:

1.  Open your implementation or integration project.

2.  Run this command to open the **Project Properties** tab:

    ```command
    MuleSoft: Open Mule Project Properties
    ```

> [!NOTE] Connector compatibility is checked against the selected Mule runtime and Java versions.
> Compatibility issues appear after you apply changes in **Project Properties**.

### Install Additional Mule Runtime Versions

Bundled Mule runtime versions enable instant project opening and design. If you need specific Mule
versions for running or debugging your applications, install these additional versions.

To install a specific Mule runtime version:

1.  Open **Command Palette** by pressing Cmd+Shift+P on Mac, or Ctrl+Shift+P on Windows.

2.  Run the command:

    ```command
    MuleSoft: Install Runtime
    ```

> [!NOTE] The dropdown in project creation and **Project Properties** shows only locally available
> Mule runtime versions. After installing additional Mule runtime versions, they appear in these
> dropdowns for future use.

## Triggering Flows in Your Development Environment

When your integration or implementation builds successfully within Anypoint Code Builder, the
application deploys to your local development environment.

Configure the **HTTP Listener** from Anypoint Connector for HTTP (HTTP
Connector) to trigger the execution of a flow in a deployed application. Or trigger the flow locally
from the built-in terminal in Anypoint Code Builder, or from a VS Code extension like Thunder
Client.

A **Scheduler**, a **Flow Ref**, or any connector trigger or message source can initiate a flow
execution. These components serve as entry points that listen for specific events or time intervals
to start the flow logic.

### Before You Begin

- Complete Getting Started with Anypoint Code Builder.

- Make sure an integration or implementation project with an HTTP Listener (`<http:listener/>`) is
  available in Anypoint Code Builder.

  To create a project, see Creating Integrations or
  Implementing APIs, or follow
  Take Your API Specification from Design Through Deployment.

### URLs for Triggering a Flow from an HTTP Listener

For integrations and implementations that you build and deploy during the development process, the
URL to use for triggering an HTTP Listener differs depending on whether the listener is within the
configuration XML for a scaffolded interface that is generated from an API specification or within a
configuration XML file that does not implement a scaffolded interface.

Typically, for apps that use an HTTP Listener, you configure the host to `0.0.0.0` and the port to
`8081`. If port `8081` is in use by another application, you can use a similar port, such as `8082`.

- Trigger a flow within a configuration XML that _does not_ contain a scaffolded interface by using
  a URL similar to this one from the terminal:

  http://localhost:8081/mypath

  The port and host are defined in the `<http:listener-connection/>` element, and the endpoint is
  defined by the `path` attribute in the `<http:listener/>` element:

  ```xml
  <http:listener-config name="inbound-request"
        doc:name="Listener Config" doc:id="b5c62f">
    <http:listener-connection host="0.0.0.0" port="8081"/>
  </http:listener-config>
  <flow name="myFlow">
      <http:listener path="mypath" config-ref="inbound-request" doc:name="HTTP /flights" />
      ...
  </flow>
  ```

- Trigger a flow from the listener within a scaffolded interface by using a URL similar to this one
  from the terminal:

  http://localhost:8081/api/my-endpoint

  Notice `/api/my-endpoint` in the example. For this case, the endpoint is defined within the `name`
  attribute of a `<flow/>` element in the interface, and `api` is defined in an HTTP Listener in the
  interface.

  For example, assume that a flow in a scaffolded interface references a flow (`getFlights`):

  ```xml
  <flow name="get:\flights:american-flights-api-config">
      <flow-ref name="getFlights"/>
      <logger level="INFO" message="get:\flights:american-flights-api-config" />
  </flow>
  ```

  Also assume that the `getFlights` flow resides in an XML configuration file for the
  implementation:

  ```xml
  <flow name="getFlights" >
      <set-payload value="Hello Flights!" doc:name="Set payload" doc:id="gwdsmi" />
      <logger doc:name="Logger" doc:id="dnitvb" message="#[payload]"/>
  </flow>
  ```

  The URL to trigger this flow uses `flights` as the endpoint:

  http://localhost:8081/api/flights

  The URL adds `/api` before the `/flights` endpoint to make the request through the
  `<http:listener/>` in the interface. Generally, a listener is located before the router, as in
  this example:

  ```xml
  <apikit:config name="american-flight-api-config"
                 api="resource::bc64acc7-41ad-43b7-9e0a-092182b03271:American-Flight-API:1.0.0:raml:zip:american-flight-api.raml"
                 outboundHeadersMapName="outboundHeaders"
                 httpStatusVarName="httpStatus" />
  <flow name="american-flight-api-main">
      <http:listener config-ref="inbound-request" path="/api/*"> (1)
          <http:response statusCode="#[vars.httpStatus default 200]">
              <http:headers>#[vars.outboundHeaders default {}]</http:headers>
          </http:response>
          <http:error-response statusCode="#[vars.httpStatus default 500]">
              <http:body>#[payload]</http:body>
              <http:headers>#[vars.outboundHeaders default {}]</http:headers>
          </http:error-response>
      </http:listener>
      <apikit:router config-ref="american-flight-api-config" /> (2)
      ...
  </flow>
  ```

|  |  |
|---|---|
| 1 | Within the listener (`<http:listener/>`), the attribute `path="/api/*"` is set automatically during the scaffolding process. |
| 2 | The router (`<apikit:router/>`) is located after the listener in the scaffolded interface within the configuration XML. |

### Trigger a Flow

Use the terminal in Anypoint Code Builder to trigger a flow through an HTTP Listener in an
integration or implementation project that is deployed locally.

> [!TIP] The examples in this procedure show how to trigger the flow with a `curl` command from the
> terminal. You can also use Thunder Client, a third-party extension for VS Code, to trigger a flow
> with the same URLs.

Before attempting to trigger a flow, review
URLs for Triggering a Flow from an HTTP Listener, and verify that you meet the
prerequisites in Before You Begin.

1.  Before starting your Mule app, confirm that the connection to the listener is successful:

    From the code editor, above the HTTP Listener configuration (`<http:listener-config/>`), click
    **Test Connection**.

    - If the test succeeds, you see a **Connection is valid** message.

    - If the connection fails, an error message indicates that the connection was unsuccessful. If
      the app is running when you click **Test Connection**, this error message appears:
      `Invalid Connection Got status code: 500 when trying to resolve a Mule Runtime operation. Reason: 'Internal Server Error.`

6.  At the command prompt, provide a `curl` command to trigger the flow.

    - To trigger a flow from an HTTP Listener that doesn’t reside within an interface, use `curl`
      with a URL similar to this one:

      $ curl localhost:8081/mypath

      Use `localhost` instead of `0.0.0.0`. Get more information about
      triggering the endpoint.

      If successful, the command returns a response.

    - To trigger a flow from an HTTP Listener that resides in a scaffolded interface, use `curl`
      with a URL similar to this one:

      $ curl http://localhost:8081/api/mypath2

      Use `localhost` instead of `0.0.0.0`, and add the listener `path` for before the router (such
      as `api` for most scaffolded interfaces) and the endpoint (such as `mypath2`) to the URL. Get
      more information about triggering the endpoint.

### Trigger a Scheduler Component On Demand

A Scheduler component waits for its configured fixed frequency or cron expression to elapse before
triggering a flow. Instead of waiting for that interval during local testing, you can trigger a
Scheduler on demand while your Mule application is running, whether or not you’re in a debug
session.

This feature invokes the Scheduler’s own trigger, it doesn’t bypass the Scheduler or create a
temporary schedule. The flow runs exactly as it would on a natural tick, so breakpoints and
interceptors behave the same way.

The on-demand trigger is for local testing only. It’s not available for applications deployed to a
remote environment. In a multi-project workspace, the trigger is scoped to the app that owns the
Scheduler, so triggering a Scheduler in one app doesn’t affect Schedulers in other running apps.

#### Trigger a Single Scheduler

To trigger one Scheduler on demand from the canvas:

4.  On the Scheduler component, click the **Trigger** ()
    button.

    After triggering the Scheduler, the button changes to **Re-trigger**
    () so you can fire the Scheduler again.

The flow runs exactly as it does when the Scheduler triggers naturally. If you set a breakpoint on a
processor in the flow, execution pauses there just as it does for a scheduled run.

> [!TIP] To trigger every Scheduler in the running application at once, use the **Trigger All
> Schedulers** button on the **Run and Debug** toolbar instead of triggering each Scheduler
> individually.

## Debugging Mule Applications

In Anypoint Code Builder, the embedded debugger pauses Mule flows so you can inspect payloads and
variables, evaluate DataWeave expressions, and step through processors in the XML editor or on the
canvas. Set breakpoints in configuration files or on components, run in debug mode, step through
execution with the debug toolbar, and hot deploy updates while the runtime stays up. The result is
faster diagnosis: you confirm event state and processor behavior before you ship your integration.

Complete these steps:

1.  Set breakpoints to pause the execution of a flow at lines that you want to
    inspect or fix.

    Breakpoints are markers that you add on line numbers in a configuration XML file for a Mule
    application that you are developing.

2.  Run the application in debug mode.

3.  Start execution of a flow in your Mule application.

    For example, trigger an HTTP Listener, or trigger a Scheduler on demand instead of waiting for
    its next tick. See
    int-trigger-flows.adoc#trigger-scheduler-on-demand.

4.  When the execution stops at a breakpoint, use the debug toolbar to navigate,
    inspect, and fix issues.

5.  After addressing an issue at a breakpoint, redeploy (hot deploy) the running
    instance of your application.

6.  Execute your flow again, and continue debugging until you address all issues.

7.  Stop the debug session.

### Before You Begin

- Set up and access Anypoint Code Builder.

- Create an integration.

### Debugger View Overview

Use **Run and Debug** to open the view. Start a Mule debug session (**Start Debugging**, F5),
inspect runtime state, and manage breakpoints. Keyboard shortcut to open the view: Cmd+Shift+D (Mac)
or Ctrl+Shift+D (Windows).

The **Debug Console** tab in the lower panel area lets you
evaluate DataWeave while execution is paused. See
Evaluate DataWeave While Debugging.

#### Panels and Tools

- **Debug toolbar** — Appears when a session is active. See Debug Toolbar for
  **Continue**, **Step Over**, **Step Into**, **Step Out**, **Restart**, and **Stop**.

- **Variables** — Tree of the current Mule event: payload, attributes, variables, and component
  parameters (such as the current processor name). See
  Inspect Variables and the Mule Event for how errors, MIME types,
  copying, and editing appear in this release.

- **Watch** — Pin DataWeave expressions that reevaluate whenever execution
  pauses.

- **Call Stack** — Frames for the current execution context (including multiple threads when
  applicable).

- **Breakpoints** — Breakpoints listed by file and line, including
  **All Exceptions** when you want to stop on any thrown exception.

- **Terminal** — Maven build output and deployment messages for the embedded Mule runtime.

Breakpoints appear in the XML editor and on canvas processors. For more information about adding
breakpoints from the editor or the canvas, see Add a Breakpoint.

#### Canvas Behavior While Debugging

When execution pauses at a breakpoint or after a step, the flow canvas shows which processor is
active. The paused processor is outlined so you can see where the runtime stopped. The canvas view
scrolls as needed to keep that processor in view when a pause occurs so you can follow execution
without searching the diagram manually.

#### Source Editor and Multiple Configuration Files

Projects can split flows across several Mule configuration XML files. When a breakpoint is hit or
you step, the editor opens or switches focus to the XML file that contains the flow and processor
that is actually executing, and the canvas shows that configuration. Stepping through a `<flow-ref>`
into a referenced flow opens the file that declares that referenced flow and updates the canvas
accordingly. If the referenced flow is in an imported Mule project dependency, it opens in a
read-only canvas and XML view.

### Inspect Variables and the Mule Event

While execution is paused, use the **Variables** tree to inspect payload, attributes, `vars`, and
related values.

When the Mule event has an error in scope, the **Variables** view includes error information so you
can diagnose failures without hunting through unrelated nodes. When no error is present, that
error-specific presentation is omitted.

Payloads and values that use common text-based MIME types (such as `application/json`, `text/xml`,
and `text/plain`) appear as readable text in the tree. Values that are truly binary are shown with a
compact placeholder instead of a long byte dump.

To reuse a value elsewhere, copy it from the tree using the context menu action that copies the
value as JSON. Copied JSON is valid for typical parsers. The string escaping matches what you paste
into external tools.

Change some variable values during a pause. Use the variable context menu to edit the value inline
where the debugger allows it. After resuming, the running application uses the updated value.

### Add a Breakpoint

A breakpoint enables you to pause your Mule application at a specific place to learn more about what
is happening. You can either add a breakpoint to a configuration XML file or to a component in the
canvas UI.

#### Add a Breakpoint in a Configuration File

To add a breakpoint in a configuration XML file:

1.  In Anypoint Code Builder, on the Explorer view, open your configuration XML file, for example,
    `my-project-name.xml`.

4.  Add more breakpoints on other lines as needed.

    Registered breakpoints appear in the **Run and Debug** view under **Breakpoints**, grouped by
    file and line, with checkboxes to enable or disable each one.

#### Add a Breakpoint to a Component in the Canvas UI

To add a breakpoint to a component in the canvas UI:

1.  In Anypoint Code Builder, on the Explorer view, open your configuration XML file, for example,
    `flights-implementation.xml`.

#### Add a Breakpoint to a Batch Component

Add a breakpoint to a batch component in the canvas UI or in a configuration XML file:

1.  In Anypoint Code Builder, on the Explorer view, open your configuration XML file, for example,
    `batch-example.xml`.

5.  Run the application in debug mode.

    When execution reaches the breakpoint, processing pauses so you can inspect variables, payloads,
    and the execution state in the Debug panel.

> [!NOTE] Batch execution is concurrent. Multiple record blocks can be processed in parallel, so
> breakpoints can trigger on different threads. The Debug panel displays each thread context so you
> can inspect each execution path.

### Set a Conditional Breakpoint

A conditional breakpoint uses a DataWeave expression, so execution pauses at that line only when the
expression evaluates to `true`.

To set or change a breakpoint condition:

1.  Add a breakpoint in the code editor. See Add a Breakpoint.

The gutter context menu for a breakpoint also includes **Remove Breakpoint**, **Disable
Breakpoint**, and **Run to Line**.

To review a condition later, hover over the breakpoint in the gutter. A tooltip shows the configured
expression in the form `Condition:` followed by your DataWeave expression.

### Stop When an Exception Is Thrown

You can configure the debugger to pause whenever any exception is thrown, which helps you inspect
failures without adding breakpoints to every path.

1.  Open **Run and Debug**.

### Run Your Application in Debug Mode

After setting up your debug conditions, run a debug session and evaluate your Mule application at
each breakpoint:

> [!NOTE] Selecting **Run** > **Start without Debugging** produces an error.

Anypoint Code Builder packages your application and deploys the application to the embedded Mule
runtime engine. The integrated terminal shows Maven and deployment progress, and the status bar
indicates that the application is running.

Use the controls on the debug toolbar to drive the session after you trigger your
flow.

### Debug Toolbar

When a Mule debug session is active, the debug toolbar provides:

1.  **Continue** (F5) — Runs until the next breakpoint or the end of the application.

2.  **Step Over** (F10) — Runs to the next processor in the current flow and pauses there.

    At a **Flow Ref** component (`<flow-ref/>`), **Step Over** doesn’t enter the referenced flow. It
    moves to the next processor after the reference in the same flow instead.

    Step Over Details

    **Configuration XML example**:

    ```xml
    <flow name="flow1" doc:name="Flow" >
      <http:listener path="greet" config-ref="HTTP_Listener_config" doc:name="Listener"/>
      <flow-ref name="myNewFlow" /> (1)
      <logger doc:name="Logger1" message="test1"/> (2)
    </flow>

    <flow name="myNewFlow" doc:name="Flow" >
      <logger doc:name="Logger2" message="test2"/>
    </flow>
    ```

    **Step Over behavior**:

|  |  |
|---|---|
| 1 | Skips `<flow-ref/>` logic |
| 2 | Reaches `<logger/>` named `Logger1` |

3.  **Step Into** (F11) — Enters the next processor, including following a `<flow-ref/>` into the
    referenced flow.

    When you step into a flow reference, Anypoint Code Builder opens the Mule configuration file
    that declares that referenced flow, moves the canvas to that flow, and pauses on the first
    processor inside it. If the referenced flow is in an imported Mule project dependency, the
    dependency flow opens in a read-only canvas and XML view. You can step through its processors,
    and stepping continues in the caller flow where appropriate after you step through the
    referenced flow.

    Step Into Details

    **Configuration XML example**:

    ```xml
    <flow name="flow1" doc:name="Flow" >
      <http:listener path="greet" config-ref="HTTP_Listener_config" doc:name="Listener"/>
      <flow-ref name="myNewFlow" /> (1)
      <logger doc:name="Logger1" message="test1"/> (3)
    </flow>

    <flow name="myNewFlow" doc:name="Flow" >
      <logger doc:name="Logger2" message="test2"/> (2)
    </flow>
    ```

    **Step Into behavior**:

|  |  |
|---|---|
| 1 | Enters `<flow-ref/>` to follow logic to `myNewFlow` |
| 2 | Reaches `Logger2` in next flow, `myNewFlow` |
| 3 | Returns to flow `flow1` to reach `Logger1` |

4.  **Step Out** (Shift+F11) — Leaves the current flow and returns toward the caller when possible;
    if there is no caller frame, behaves like **Continue**.

5.  **Restart** (Shift+Cmd+F5 on Mac, Shift+Ctrl+F5 on Windows) — Stops and restarts without picking
    up new Maven dependencies from `pom.xml`.

6.  **Stop** (Shift+F5) — Ends the application. The next debug session repackages the app if you
    added connector or dependency changes.

### Evaluate DataWeave While Debugging

While execution is paused, you can run DataWeave against the current Mule event from the **Debug
Console** or from pinned entries in the **Watch** panel. For the variables available in those
expressions, see Predefined Mule event variables.

#### Use the Debug Console

1.  Start a debug session and pause execution at a breakpoint or after a step. See
    Run Your Application in Debug Mode and Debug Toolbar.

3.  Ensure the input is set to **Expression**. Type a DataWeave expression and press Enter to
    evaluate it against the current message, attributes, variables, and other values visible to the
    debugger at the pause.

    The console shows each expression you run and its evaluated result for the current pause.

Use the **Debug Console** for checking the steps as you debug through a flow.

#### Use the Watch Panel

2.  Add an entry with **+** and enter a DataWeave expression.

    Whenever execution pauses, the debugger reevaluates each watch expression and shows the result
    next to the expression, similar to the **Debug Console**.

    Watch expressions typically persist for later debug sessions in the same workspace, so you can
    keep inspecting the same values across runs.

Use the **Watch** panel for values you want to track on every pause without retyping them.

### Perform a Hot Deploy When Debugging

As you debug your application, periodically perform a hot deployment. A hot deployment updates a
running instance of your application but does not package new dependencies, such as new connector
dependencies in your `pom.xml`.

To perform a hot deploy:

1.  Ensure your Mule application is running.

2.  Make an update to your application.

### Stop a Debug Session

To stop your debug session, use **Stop** on the debug toolbar (Shift+F5), or open **Run and Debug**
and choose the stop action for the active Mule session.

The status bar no longer indicates that the application is running.

## Pass Runtime Properties and Arguments to Mule Applications

Configure runtime behavior, secure sensitive data, and test different environments by passing
properties and arguments to Mule applications running locally in Anypoint Code Builder.

Use command-line properties to switch between development, sandbox, and production configurations,
provide encryption keys for secure properties, and override default values without modifying
application code.

You can pass properties when running Mule applications locally through different methods.

- Global default arguments: Apply the same arguments to all Mule
  applications

- Project-specific launch configurations: Configure arguments for individual
  projects or create multiple configurations with different settings

### Configure Global Default Arguments

Configure arguments that apply to all Mule application runs in Anypoint Code Builder. Use this
approach when you consistently need the same encryption key or environment setting across all
projects during local development.

To configure global default arguments:

1.  Open Mule settings:

2.  If an API specification is open in the Explorer panel, close the project to avoid a
    synchronization error when you switch clouds.

4.  Find the **Mule › Runtime: Default Arguments** setting.

    ```text
    -M-Dencryption.key=myEncryptionKey123
    ```

    To add multiple arguments, separate them with spaces:

    ```text
    -M-Dencryption.key=myEncryptionKey123 -M-Denv=dev -M-Dhttp.port=8082
    ```

6.  Run or debug your Mule application:

#### Understand Property Syntax

The `-M-D` prefix passes system properties to the Java Virtual Machine (JVM) that runs Mule Runtime
engine. These properties become available throughout your Mule application and can be referenced in
configuration XML files.

When configuring properties in the **Runtime: Default Arguments** field:

- Use the `-M-D` prefix followed by the property name and value: `-M-Dname=value`

- Separate multiple properties with spaces

- Avoid quotes around values unless the value contains spaces

- Property names are case-sensitive

Common examples:

```text
-M-Dencryption.key=mySecretKey
-M-Denv=dev
-M-Dhttp.port=8081
-M-Ddatabase.host=localhost
-M-Dmule.env=development
```

### Configure Project-Specific Launch Configurations

Configure arguments for individual projects or create multiple run configurations with different
settings for the same project. Use this approach when different projects require different
configurations, or to test the same project with different property values.

Launch configurations reside in the `.vscode/launch.json` file in your project directory and apply
only to that project.

#### Create or Modify a Launch Configuration

To configure project-specific arguments:

4.  Add or modify the `mule.runtime.args` property to include your arguments:

    ```json
    {
      "version": "0.2.0",
      "configurations": [
        {
          "type": "mule-xml-debugger",
          "request": "launch",
          "name": "Debug Mule Application",
          "mule.project": "${workspaceFolder}",
          "mule.home": "${config:mule.homeDirectory}",
          "mule.runtime.args": "${config:mule.runtime.defaultArguments} -M-Dencryption.key=myKey -M-Denv=dev"
        }
      ]
    }
    ```

5.  Save the `launch.json` file.

6.  Run or debug your application by selecting the configuration from the **Run and Debug** view.

#### Test the Same Project with Different Property Values

Create multiple launch configurations with different property values to test various environments
without editing the configuration file each time. For conceptual information about creating and
managing launch configurations, see
Running Multiple Mule Applications Concurrently.

The key difference when configuring properties is to vary the `mule.runtime.args` values for each
configuration:

```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "type": "mule-xml-debugger",
      "request": "launch",
      "name": "Debug - Development",
      "mule.project": "${workspaceFolder}",
      "mule.home": "${config:mule.homeDirectory}",
      "mule.runtime.args": "${config:mule.runtime.defaultArguments} -M-Denv=dev -M-Dhttp.port=8081"
    },
    {
      "type": "mule-xml-debugger",
      "request": "launch",
      "name": "Debug - Sandbox",
      "mule.project": "${workspaceFolder}",
      "mule.home": "${config:mule.homeDirectory}",
      "mule.runtime.args": "${config:mule.runtime.defaultArguments} -M-Denv=sandbox -M-Dhttp.port=8082"
    }
  ]
}
```

Switch between configurations using the dropdown in the **Run and Debug** view.

#### Use Environment Variables in Launch Configurations

Reference environment variables defined on your system to avoid hardcoding sensitive values in
`launch.json`:

```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "type": "mule-xml-debugger",
      "request": "launch",
      "name": "Debug with Environment Variables",
      "mule.project": "${workspaceFolder}",
      "mule.home": "${config:mule.homeDirectory}",
      "mule.runtime.args": "${config:mule.runtime.defaultArguments} -M-Dencryption.key=${env:ENCRYPTION_KEY} -M-Denv=${env:MULE_ENV}"
    }
  ]
}
```

Reference environment variables using the `${env:VARIABLE_NAME}` syntax. The example configuration
references `ENCRYPTION_KEY` and `MULE_ENV` from your system environment.

### Common Use Cases and Examples

These examples demonstrate common scenarios for passing runtime properties and arguments, such as
configuring HTTP listener ports and database connection parameters.

For examples of passing encryption keys and switching between environment-specific property files,
see Defining and Securing Properties for a Mule Application.

#### Example: Set HTTP Listener Port Dynamically

Set the HTTP listener port at runtime without modifying your configuration XML:

Global default arguments:

```text
-M-Dhttp.port=8082
```

Launch configuration:

```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "type": "mule-xml-debugger",
      "request": "launch",
      "name": "Debug on Port 8082",
      "mule.project": "${workspaceFolder}",
      "mule.home": "${config:mule.homeDirectory}",
      "mule.runtime.args": "${config:mule.runtime.defaultArguments} -M-Dhttp.port=8082"
    }
  ]
}
```

Reference the property in your HTTP listener configuration:

```xml
<http:listener-config name="HTTP_Listener_config" >
  <http:listener-connection host="0.0.0.0" port="${http.port}" />
</http:listener-config>
```

#### Example: Increase JVM Heap Size

Increase the maximum JVM heap size when running memory-intensive Mule applications locally. Use the
`-M-Xmx` flag to set the maximum heap and `-M-Xms` to set the initial heap.

Global default arguments:

```text
-M-Xms512m -M-Xmx2g
```

Launch configuration:

```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "type": "mule-xml-debugger",
      "request": "launch",
      "name": "Debug with Increased Heap",
      "mule.project": "${workspaceFolder}",
      "mule.home": "${config:mule.homeDirectory}",
      "mule.runtime.args": "${config:mule.runtime.defaultArguments} -M-Xms512m -M-Xmx2g"
    }
  ]
}
```

You can combine heap size flags with other arguments, such as environment properties or encryption
keys:

```text
-M-Xmx2g -M-Denv=dev -M-Dencryption.key=myKey
```

#### Example: Provide Database Connection Parameters

Provide database connection parameters at runtime to switch between local and remote databases:

Global default arguments:

```text
-M-Ddb.host=localhost -M-Ddb.port=3306 -M-Ddb.name=mydb
```

Launch configurations for different databases:

```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "type": "mule-xml-debugger",
      "request": "launch",
      "name": "Debug with Local Database",
      "mule.project": "${workspaceFolder}",
      "mule.home": "${config:mule.homeDirectory}",
      "mule.runtime.args": "${config:mule.runtime.defaultArguments} -M-Ddb.host=localhost -M-Ddb.port=3306 -M-Ddb.name=mydb"
    },
    {
      "type": "mule-xml-debugger",
      "request": "launch",
      "name": "Debug with Remote Database",
      "mule.project": "${workspaceFolder}",
      "mule.home": "${config:mule.homeDirectory}",
      "mule.runtime.args": "${config:mule.runtime.defaultArguments} -M-Ddb.host=remote-db.example.com -M-Ddb.port=3306 -M-Ddb.name=proddb"
    }
  ]
}
```

Reference these properties in your database configuration:

```xml
<db:config name="Database_Config" >
  <db:my-sql-connection
    host="${db.host}"
    port="${db.port}"
    database="${db.name}"
    user="${db.user}"
    password="${secure::db.password}" />
</db:config>
```

### Configure Shared Encryption Keys Across a Workspace

When you have multiple Mule projects in the same workspace that use the same encryption key,
configure it once at the workspace level instead of duplicating it in each project’s launch.json.

Use the approach that better applies to your workflow and security requirements.

- Workspace Settings: Configure the encryption key in your workspace
  settings.json. All projects inherit the setting automatically.

- Environment Variable: Store the key as an OS environment
  variable in your shell profile. Use this method to keep encryption keys completely out of
  version-controlled files or if you need machine-specific configuration.

- Multi-Root Workspace: Configure the encryption key directly in a
  .code-workspace file. Use this approach when working with multiple Mule projects open
  simultaneously in a multi-root workspace.

#### Use Workspace Settings

Add the encryption key to your workspace `settings.json` so all projects inherit it.

1.  In your `.code-workspace` file or `.vscode/settings.json` at the workspace root, add the key.

    ```json
    {
      "settings": {
        "mule.runtime.defaultArguments": "-M-Dencryption.key=MuleSecureKey024"
      }
    }
    ```

2.  Reference the shared setting in each project’s `launch.json`.

    ```json
    {
      "mule.runtime.args": "${config:mule.runtime.defaultArguments}"
    }
    ```

#### Use an Environment Variable

Set the key as an OS environment variable in your shell profile (`~/.zshrc` or `~/.bash_profile`)

1.  Run this command.

    ```bash
    export MULE_ENCRYPTION_KEY="MuleSecureKey024"
    ```

2.  Reference the key in the workspace `launch.json`:

    ```json
    {
      "version": "0.2.0",
      "configurations": [
        {
          "type": "mule-xml-debugger",
          "request": "launch",
          "name": "Debug with Environment Variable",
          "mule.project": "${workspaceFolder}",
          "mule.home": "${config:mule.homeDirectory}",
          "mule.runtime.args": "${config:mule.runtime.defaultArguments} -M-Dencryption.key=${env:MULE_ENCRYPTION_KEY}"
        }
      ]
    }
    ```

#### Use a Shared Launch Configuration in Multi-Root Workspaces

To configure a shared encryption key in a multi-root workspace:

1.  Open or create your `.code-workspace` file.

2.  Add a `launch` section to the workspace configuration with the encryption key:

    ```json
    {
      "folders": [  (1)
        { "path": "salesforce-sync" },
        { "path": "netsuite-integration" },
        { "path": "slack-notifications" }
      ],
      "launch": {  (2)
        "configurations": [
          {
            "type": "mule-xml-debugger",
            "request": "launch",
            "name": "Run Mule App (Shared Key)",  (3)
            "noDebug": true,
            "mule.projects": ["${workspaceFolder}"],
            "mule.runtime.args": "${config:mule.runtime.defaultArguments} -M-Dencryption.key=MuleSecureKey024"  (4)
          }
        ]
      }
    }
    ```

|  |  |
|---|---|
| 1 | List the relative paths to each Mule project in your workspace |
| 2 | Add the launch configuration section with the shared encryption key |
| 3 | Name that appears in the Run and Debug dropdown |
| 4 | Replace `MuleSecureKey024` with your encryption key |

3.  Save the workspace file.

When you select **Run Mule App (Shared Key)** from the Run and Debug dropdown, Code Builder applies
the shared encryption key to whichever project is active.

#### Protect Workspace Configuration in .gitignore

If your workspace settings contain sensitive values, add them to `.gitignore`:

```gitignore
# Workspace config (may contain encryption key)
*.code-workspace
.vscode/settings.json
```

#### Re-encrypt All Projects After Key Rotation

When you rotate the shared key, re-encrypt every secure properties file across all projects:

```bash
NEW_KEY="NewSharedKey2025!"

# For each project in the workspace:
for project in salesforce-sync netsuite-integration slack-notifications; do
  FILE="$project/src/main/resources/prod.secure.properties"
  if [ -f "$FILE" ]; then
    echo "Re-encrypting: $FILE"
    # Decrypt each value with old key, re-encrypt with new key
    # (or use a local backup file with plaintext to re-encrypt)
  fi
done
```

Then update the single workspace-level key reference and all projects work immediately.

## Running Multiple Mule Applications Concurrently

Run multiple Mule applications concurrently in the same local runtime instance by creating a custom
run or debug configuration in your workspace. Use this approach to test service-to-service
interaction and verify end-to-end integration behavior without deploying to remote environments.

To run related projects together, configure a workspace-level launch configuration that includes all
target projects. After you create the configuration, you can reuse it for both run and debug
sessions.

To create run configurations for multiple projects using MuleSoft Vibes, see
Running Multiple Local Integration Projects with MuleSoft Vibes.

### Before You Begin

- Create a multi-root workspace that contains all the Mule projects you want to
  run concurrently.

### Create a Run Configuration for Multiple Projects

To create a workspace-level run configuration:

6.  Update the `mule.projects` field to include all project folders you want to run concurrently.

    Use this format
    `"${workspaceFolder:project1FolderName}", "${workspaceFolder:project2FolderName}"`

    Replace `project1FolderName` and `project2FolderName` with the actual folder names of your
    projects. Add additional project folders separated by commas as needed.

7.  Copy the `mule.projects` values and paste them into the `mule.projects` field inside the
    **Debug** configuration.

    This step ensures the same projects are available when you run in debug mode.

    Example configuration:

    ```json
    "version": "0.2.0",
        "configurations": [

          {
            "type": "mule-xml-debugger",
            "request": "launch",
            "name": "Run Multiple Applications",
            "noDebug": true,
            "mule.projects": [
              "${workspaceFolder:first-project}",
              "${workspaceFolder:second-project}"
            ],
            "mule.runtime.args": "${config:mule.runtime.defaultArguments}"
          },
          {
            "type": "mule-xml-debugger",
            "request": "launch",
            "name": "Debug Multiple Applications",
            "mule.projects": [
              "${workspaceFolder:first-project}",
              "${workspaceFolder:second-project}"
            ],
            "mule.runtime.args": "${config:mule.runtime.defaultArguments}"
          }
        ]
    ```

8.  Save the `.code-workspace` file.

    The new configuration now appears in the launch configuration dropdown in the **Run and Debug**
    panel.

### Run the Configuration

After you create the configuration, run it to start all included projects in the same local runtime
instance:

### Update an Existing Configuration

To modify which projects run in the configuration:

1.  Open your `.code-workspace` file.

2.  Locate the launch configuration by name.

3.  Update the `mule.projects` array to add, remove, or reorder projects.

4.  Save the file.

    The updated configuration is immediately available in the **Run and Debug** panel.

## Command Reference

Anypoint Code Builder provides a set of commands through the Command Palette.

### MuleSoft Commands

#### Platform Commands

- Open MuleSoft Vibes from the Command Palette.

  ```command
  MuleSoft: Open MuleSoft Vibes
  ```

- Export troubleshooting information, including logs and workspace details. See
  Export Troubleshooting Information.

  ```command
  MuleSoft: Export Troubleshooting Information
  ```

- Import an existing Studio workspace into Anypoint Code Builder.

  ```command
  MuleSoft: Import Studio Workspace
  ```

- Log in to Anypoint Platform from. See Log in through the Command Palette.

  ```command
  MuleSoft: Login to Anypoint Platform
  ```

  ```command
  MuleSoft: Open ACB Settings
  ```

  ```command
  MuleSoft: Show Welcome
  ```

- Open project dependencies in the Explorer view.

  ```command
  MuleSoft: Show Project dependencies
  ```

#### Integration Commands

- Deploy an integration or implementation to CloudHub. See
  Deploy an App to CloudHub.

  ```command
  MuleSoft: Deploy Mule Project to CloudHub
  ```

- Start an integration project. You can also start an integration project from the UI. See
  Creating Integrations.

  ```command
  MuleSoft: Develop an Integration
  ```

- Create a shareable or deployable JAR from your project. See
  Export Mule Project.

  ```command
  MuleSoft: Export Mule Project
  ```

- Download a supported Java Development Kit version for local development.

  ```command
  MuleSoft: Download JDK
  ```

- Download a Mule runtime version for local development.

  ```command
  MuleSoft: Download Mule Runtime
  ```

- Import an API spec from Exchange and scaffold it into an implementation project. See
  Scaffold an API and Create an Integration Project.

  ```command
  MuleSoft: Implement an API Specification
  ```

- Import a connector, REST or GraphQL library, or DataWeave library from Anypoint Exchange. See
  examples in
  Import a Connector from Exchange,
  Import an API Spec into an Existing Implementation Project,
  and Import a DataWeave Library.

  ```command
  MuleSoft: Import Asset from Exchange
  ```

- Import a JAR file for a Mule project and load it into a workspace. See
  Importing Projects into Anypoint Code Builder.

  ```command
  MuleSoft: Import a Mule Project
  ```

- Open custom metadata management for a Mule project.

  ```command
  MuleSoft: Manage Custom Metadata
  ```

- Publish an integration project to Anypoint Exchange.

  ```command
  MuleSoft: Publish Mule Project to Exchange
  ```

- Save and hot-deploy to a local Mule runtime.

  ```command
  MuleSoft: Save and Hot-deploy to Local Runtime
  ```

- Run a Mule application locally.

  ```command
  MuleSoft: Run Mule Application
  ```

- Run a saved multi-project launch configuration from your workspace. See
  Running Multiple Local Integration Projects with MuleSoft Vibes.

  ```command
  MuleSoft: Run Multi-Project Configuration
  ```

- Open Mule project properties.

  ```command
  MuleSoft: Open Mule Project Properties
  ```

  ```command
  MuleSoft: Toggle Canvas Layout (Classic/Descriptive)
  ```

#### API and Governance Commands

- Add an API spec fragment from Exchange to the project directory to include the fragment in your
  spec. See
  Add a Fragment from Exchange to Your Project.

  ```command
  MuleSoft: Add Fragment dependency from Exchange
  ```

  ```command
  MuleSoft: Show API Console
  ```

- Start an API design project. You can also start the project from the UI. See
  Creating and Importing API Specifications.

  ```command
  MuleSoft: Design an API
  ```

- Scaffold a local API spec project into an implementation project. See
  Scaffold an API Spec into a New Implementation Project.

  ```command
  MuleSoft: Implement this local API
  ```

- Import an API spec from MuleSoft VCS. See
  Import an API Specification from MuleSoft VCS.

  ```command
  MuleSoft: Import API Specification from MuleSoft VCS
  ```

- Open API project properties.

  ```command
  MuleSoft: Open API Project Properties
  ```

- Publish an API project to Anypoint Exchange. See
  Publish an API spec to Exchange.

  ```command
  MuleSoft: Publish API Project to Exchange
  ```

- Re-scaffold an API after updating a local API spec. See
  Re-Scaffold the API Spec.

  ```command
  MuleSoft: Re-scaffold this local API
  ```

  > [!NOTE] This command is available only for API specifications that haven’t been published to
  > Anypoint Exchange. If you publish the spec to Exchange, re-scaffolding is no longer available
  > for that asset.

  ```command
  MuleSoft: Show API Governance
  ```

- Change a governance ruleset version in an API design project. For information about rulesets, see
  Validating API Specifications Against Governance Rulesets.

  ```command
  MuleSoft: Change Ruleset Version
  ```

- Remove a governance ruleset from an API design project. For information about rulesets, see
  Validating API Specifications Against Governance Rulesets.

  ```command
  MuleSoft: Remove Governance Ruleset
  ```

- Run governance validation across all rulesets and rules in the project. For information about
  rulesets, see Validating API Specifications Against Governance Rulesets.

  ```command
  MuleSoft: Run Governance Validation with all Rulesets and Rules
  ```

- Sync centralized governance rulesets. For information about rulesets, see
  Validating API Specifications Against Governance Rulesets.

  ```command
  MuleSoft: Sync Centralized Rulesets
  ```

- Sync centralized rulesets and run governance validation. For information about rulesets, see
  Validating API Specifications Against Governance Rulesets.

  ```command
  MuleSoft: Sync and Run Validation
  ```

- View API conformance status in Exchange. For information about rulesets, see
  Validating API Specifications Against Governance Rulesets.

  ```command
  MuleSoft: View API Conformance Status on Exchange
  ```

#### Agent Network Commands

- Create an Agent Network project.

  ```command
  MuleSoft: Create an Agent Network Project
  ```

- Add Exchange assets to an Agent Network project.

  ```command
  MuleSoft: Add Exchange Assets to Agent Network Project
  ```

- Deploy an Agent Network project.

  ```command
  MuleSoft: Deploy Agent Network
  ```

- Publish Agent Network assets.

  ```command
  MuleSoft: Publish Agent Network Assets
  ```

- Set up Agent Network gateways.

  ```command
  MuleSoft: Set Up Agent Network Gateways
  ```

### Other Commands

Other helpful commands include the following:

- Open a project folder from the Command Palette. For examples, see
  Adding Folders to Your Home Directory.

  ```command
  File: Open Folder
  ```

  ```command
  View: Show Anypoint Code Builder
  ```

## Built-In Connectors

Anypoint connectors and modules are extensions to Mule runtime engine that process event data within
a Mule application. Connectors, unlike modules, also provide ways to connect to external systems or
services.

In Anypoint Code Builder, both integrations and implementations are Mule applications.

Anypoint connectors and modules are extensions to Mule runtime engine that process event data within
a Mule application. Connectors, unlike modules, also provide ways to connect to external systems or
services.

Built-in Anypoint connectors are available from the canvas and code editor for integration and
implementation projects. These connectors include:

- Anypoint Connector for Agent2Agent (A2A) (Beta) (<a2a:/>) (A2A
  Connector)

- Anypoint Connector for Agentforce (<ms-agentforce:/>)
  (Agentforce Connector)

- Anypoint Connector for Database (<db:/>) (Database Connector)

- Anypoint Connector for Einstein AI (<ms-einstein-ai:/>)
  (Einstein AI Connector)

- Anypoint Connector for Email (<email:/>) (Email Connector)

- Anypoint Connector for File (<file:/>) (File Connector)

- Anypoint Connector for HTTP (<http:/>) (HTTP Connector)

- Java Module (<java:/>)

- Anypoint Connector for MCP (MCP Connector) (<mcp:/>)

- Anypoint Connector for Salesforce (<salesforce:/>) (Salesforce
  Connector)

- Anypoint Connector for Salesforce Data Cloud (<sdc:/>)
  (Salesforce Data Cloud Connector)

- Anypoint Connector for Sockets (<sockets:/>) (Sockets Connector)

- Anypoint Connector for Workday (<workday:/>) (Workday Connector)

Connector XML tags start with a namespace followed by an operation, following the syntax
`namespace:operation`, such as `<db:select/>` for a Select operation in Anypoint Connector for
Database (Database Connector). For more information, see
Using Anypoint Code Builder to Configure a Connector.

Many other connectors are available from Anypoint Code Builder through Anypoint Exchange:

- US cloud (non-EU host): [Exchange (US)](https://anypoint.mulesoft.com/exchange/)

- EU cloud (EU host): [Exchange (EU)](https://eu1.anypoint.mulesoft.com/exchange/)

To find information about more connectors, see
Anypoint Connectors Overview, and
find documentation on all Anypoint connectors and modules.

## Launch Configuration Properties Reference

Configure how Mule applications run and debug locally in Anypoint Code Builder by editing the
`launch.json` file in your project’s `.vscode` folder.

Use `launch.json` configurations to:

- Pass runtime arguments (encryption keys, environment variables, JVM properties)

- Change the debug port to avoid conflicts when running multiple applications

- Create multiple run profiles for different environments (Development, QA, Production)

- Run multiple Mule applications concurrently in the same workspace

- Test the same application with different property values without editing code

### Configuration Properties Reference

This table lists some common properties for launch configurations.

| Property | Required | Description |
|---|---|---|
| `type` | Yes | Specifies the debugger type. Must be `"mule-xml-debugger"` for Mule applications or `"munit-xml-debugger"` for MUnit tests. |
| `request` | Yes | Specifies the launch type. Must be `"launch"` to start a new debug session. |
| `name` | Yes | Display name for this configuration. Appears in the Run and Debug view dropdown menu. Use descriptive names like `"Debug - Development"` or `"Run QA Environment"`. |
| `mule.project` | No | Path to a single Mule project. Use `"${workspaceFolder}"` for the current project. For multiple projects, use `mule.projects` instead. Either `mule.project` or `mule.projects` must be specified, but not both. |
| `mule.projects` | No | Array of project paths for running multiple Mule applications concurrently. Example: `["${workspaceFolder:project1}", "${workspaceFolder:project2}"]`. See Running Multiple Mule Applications Concurrently. Either `mule.project` or `mule.projects` must be specified, but not both. |
| `mule.home` | No | Path to the Mule runtime home directory. Use `"${config:mule.homeDirectory}"` to reference the configured Mule installation. Typically not needed as it defaults to the configured runtime. |
| `mule.runtime.args` | No | Command-line arguments passed to the Mule runtime JVM. Use the `-M-D` prefix for system properties and the `-M-X` prefix for JVM tuning flags. Examples: `-M-Dencryption.key=myKey` (encryption key) `-M-Denv=dev` (environment selector) `-M-Dhttp.port=8082` (HTTP listener port) `-M-Xmx2g` (maximum JVM heap size) `-M-Xms512m -M-Xmx2g` (initial and maximum JVM heap size) For more information, see Pass Runtime Properties and Arguments to Mule Applications and Defining and Securing Properties for a Mule Application. |
| `mule.debug.port` | No | Port number for the Mule debugger. Default: `6666`. Change this value when running multiple applications concurrently to avoid port conflicts. Example: `6667`, `6668`. |
| `noDebug` | No | Set to `true` to run the application without attaching the debugger. Useful for performance testing or when you don’t need breakpoint debugging. Default: `false`. |

Either `mule.project` or `mule.projects` must be specified, but not both.

### Creating Multiple Configuration Profiles

Create multiple launch configurations to test different environments without modifying your
application code. Each configuration can have different runtime arguments, debug ports, and
environment settings.

This example shows three configurations for Local Development, QA, and a Mocked environment:

```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "type": "mule-xml-debugger",
      "request": "launch",
      "name": "Debug - Local Dev",
      "mule.project": "${workspaceFolder}",
      "mule.home": "${config:mule.homeDirectory}",
      "mule.runtime.args": "${config:mule.runtime.defaultArguments} -M-Denv=dev -M-Dencryption.key=devKey123",
      "mule.debug.port": 6666
    },
    {
      "type": "mule-xml-debugger",
      "request": "launch",
      "name": "Debug - QA Environment",
      "mule.project": "${workspaceFolder}",
      "mule.home": "${config:mule.homeDirectory}",
      "mule.runtime.args": "${config:mule.runtime.defaultArguments} -M-Denv=qa -M-Dencryption.key=qaKey456",
      "mule.debug.port": 6667
    },
    {
      "type": "mule-xml-debugger",
      "request": "launch",
      "name": "Run - Mocked Services",
      "mule.project": "${workspaceFolder}",
      "mule.home": "${config:mule.homeDirectory}",
      "mule.runtime.args": "${config:mule.runtime.defaultArguments} -M-Denv=mock -M-Dmock.services=true",
      "mule.debug.port": 6666,
      "noDebug": true
    }
  ]
}
```

#### Switch Between Configurations

To switch between run configurations:

The selected configuration remains active until you select a different one.

### Configuring the Debug Port

The default debug port for Anypoint Code Builder is `6666`. Change this port when:

- Running multiple Mule applications concurrently in the same workspace

- The default port conflicts with another service on your system

- Testing port-specific debugging scenarios

#### Change the Debug Port

Add or modify the `mule.debug.port` property in your launch configuration:

```json
{
  "configurations": [
    {
      "type": "mule-xml-debugger",
      "request": "launch",
      "name": "Debug on Port 6667",
      "mule.project": "${workspaceFolder}",
      "mule.home": "${config:mule.homeDirectory}",
      "mule.runtime.args": "${config:mule.runtime.defaultArguments}",
      "mule.debug.port": 6667
    }
  ]
}
```

Each concurrent application must use a unique debug port. For example, if running three applications
simultaneously, configure them with ports `6666`, `6667`, and `6668`.

### Common Configuration Examples

These are some configuration examples for common scenarios.

#### Pass Encryption Keys for Secure Properties

```json
{
  "configurations": [
    {
      "type": "mule-xml-debugger",
      "request": "launch",
      "name": "Debug with Encryption Key",
      "mule.project": "${workspaceFolder}",
      "mule.home": "${config:mule.homeDirectory}",
      "mule.runtime.args": "${config:mule.runtime.defaultArguments} -M-Dencryption.key=mySecretKey"
    }
  ]
}
```

For more information, see
Defining and Securing Properties for a Mule Application.

#### Switch Between Environment Property Files

```json
{
  "configurations": [
    {
      "type": "mule-xml-debugger",
      "request": "launch",
      "name": "Development Environment",
      "mule.project": "${workspaceFolder}",
      "mule.home": "${config:mule.homeDirectory}",
      "mule.runtime.args": "${config:mule.runtime.defaultArguments} -M-Denv=dev"
    },
    {
      "type": "mule-xml-debugger",
      "request": "launch",
      "name": "Production Environment",
      "mule.project": "${workspaceFolder}",
      "mule.home": "${config:mule.homeDirectory}",
      "mule.runtime.args": "${config:mule.runtime.defaultArguments} -M-Denv=prod"
    }
  ]
}
```

This configuration works with property files named `dev.secure.yaml` and `prod.secure.yaml` that use
the `$site` variable in your Mule configuration XML.

#### Run Multiple Applications Concurrently

```json
{
  "configurations": [
    {
      "type": "mule-xml-debugger",
      "request": "launch",
      "name": "Run Multiple Apps",
      "noDebug": true,
      "mule.projects": [
        "${workspaceFolder:salesforce-integration}",
        "${workspaceFolder:database-service}",
        "${workspaceFolder:api-gateway}"
      ],
      "mule.runtime.args": "${config:mule.runtime.defaultArguments}"
    }
  ]
}
```

For more information, see
Running Multiple Mule Applications Concurrently.

#### Use Environment Variables

Reference OS environment variables using the `${env:VARIABLE_NAME}` syntax:

```json
{
  "configurations": [
    {
      "type": "mule-xml-debugger",
      "request": "launch",
      "name": "Debug with Env Variables",
      "mule.project": "${workspaceFolder}",
      "mule.home": "${config:mule.homeDirectory}",
      "mule.runtime.args": "${config:mule.runtime.defaultArguments} -M-Dencryption.key=${env:MULE_ENCRYPTION_KEY} -M-Denv=${env:MULE_ENV}"
    }
  ]
}
```

### Create or Open launch.json

To create or open the `launch.json` file:

3.  Edit the configuration properties as needed.

4.  Save the file.

The new or updated configuration appears in the **Run and Debug** view dropdown.

## Maven Settings in Anypoint Code Builder

Anypoint Code Builder uses Apache Maven to build and manage your Mule projects (implementation and
integration projects) and API specifications in design projects. All Maven configurations, such as
custom repositories, proxies, and server credentials, are managed through a central `settings.xml`
file.

For information about the Maven file `settings.xml`, see the
[Maven documentation](https://maven.apache.org/settings.html).

### Maven Settings File in Anypoint Code Builder

Use the Apache Maven file `settings.xml` to configure the Maven settings, such as repositories,
proxy settings, and credentials. For detailed information, see
[Settings Reference](https://maven.apache.org/settings.html) in the Apache Maven documentation.

If `settings.xml` isn’t found in that path, Anypoint Code Builder creates an empty `settings.xml`
file in the default location, `${user.home}/.m2/repository`.

### User and Internal Maven Settings in Anypoint Code Builder

Anypoint Code Builder reads its configuration from your Maven `settings.xml` file. To configure
Maven, for example, to add repositories, proxies, or credentials, edit your `settings.xml` file,
usually located in your `~/.m2/` directory.

If you troubleshoot a project in Anypoint Code Builder, export the file with any sensitive
information, such as passwords, obfuscated. See
Export Troubleshooting Information for instructions.

### Authenticating to MuleSoft Repositories

When you open a MuleSoft project that uses dependencies from the MuleSoft Enterprise Repository,
Maven requires authentication to download the artifacts. If authentication is not configured, you
receive a 401 Unauthorized error.

To configure authentication:

1.  If you don’t already have Nexus enterprise credentials, contact
    [MuleSoft Support](https://help.mulesoft.com) to request them.

2.  Optionally, encrypt your credentials.

    For instructions on encrypting your credentials to avoid storing passwords in plain text, see
    [Password Encryption](https://maven.apache.org/guides/mini/guide-encryption.html) in the Apache
    Maven documentation.

3.  Add your credentials in the `<servers>` section of your Maven `settings.xml` file.

    For detailed instructions on configuring the `settings.xml` file, see
    Configure Maven to Access MuleSoft Enterprise Repository.

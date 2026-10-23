# Troubleshooting

> Derived from the Anypoint Code Builder documentation at docs.mulesoft.com.

## Troubleshooting

Troubleshoot errors and warnings you encounter when using Anypoint Code Builder.

- Missing or Disabled Features

- Authentication Errors

- Deployment Errors

- Implementation Errors

- Mule Runtime Issues and Errors

- Project Loading Errors

- MCP Server Issues

  For other issues and workarounds, see Known Issues in the
  Anypoint Code Builder Release Notes.

For tasks that support the troubleshooting process, see:

- Check for Problems and Issues

- Check Console Logs for Extension Issues

- Export Troubleshooting Information

### Check for Problems and Issues

When you don’t know how to resolve an issue, the first step is to check for and review problems,
console output, and logs. Error messages and logs list underlying issues that can help you
understand what went wrong and what requires attention.

- To view centralized errors and warnings, open the **ACB Logs** panel. See
  View Errors and Warnings in ACB Logs.

- To view detailed logs for in-depth investigation, use the **Output** panel. See
  View Detailed Logs in the Output Panel.

- To view problems, open the **Problems** tab by pressing Cmd+Shift+m (Mac) or Ctrl+Shift+m
  (Windows).

### Check Console Logs for Extension Issues

If you encounter an issue with an Anypoint Code Builder extension, capture the console logs from the
developer tools and share them with the MuleSoft support team.

      ```command
      Developer: Toggle Developer Tools
      ```

3.  Reproduce the issue to capture the relevant log entries in the console.

4.  After the issue occurs, save or copy the logs:

    - Alternatively, click inside the console, press Ctrl+A (Cmd+A on Mac) to select all, then press
      Ctrl+C (Cmd+C on Mac) to copy the logs and paste them into a text file.

5.  Save the logs as a `.txt` file, for example, `ACB_ConsoleLogs.txt`.

6.  Attach the log file to your MuleSoft Support case.

### Export Troubleshooting Information

If the MuleSoft support team requests troubleshooting information about your project, export a
compressed file that contains your project’s workspace folders, logs, and information about
environment variables, CPU, operating system, and system properties.

2.  Provide this command:

    ```command
    MuleSoft: Export Troubleshooting Information
    ```

3.  When you receive a notification about the information that the command extracts, click
    **Continue**.

    When the process is complete, Anypoint Code Builder shows this message:

    Collecting information...: Generating compressed file

5.  Provide a copy of the file to the support team.

### Check for Anypoint Extension Pack Installation

To determine whether Anypoint Code Builder extensions are installed, check for the **Anypoint
Extension Pack** in the **Extensions: Marketplace** panel:

### Maven 401 Unauthorized Error

If Maven fails to download dependencies with a 401 Unauthorized error when opening or building a
MuleSoft project, configure authentication for the MuleSoft Enterprise Repository.

See Authenticating to MuleSoft Repositories
for instructions on configuring your credentials.

### Settings Sync Overwrites Home Directory on a New Computer

When you sync your VS Code profile to a new computer, all profile settings are transferred,
including the **Mule: Home Directory** setting. If the username on the new computer differs from the
one on the original computer, the synced path is invalid, and the extension fails to load with an
error like the following:

Error: EPERM: operation not permitted, mkdir
'C:\\Users\\<original-username>\\AnypointCodeBuilder\\java\\jdk-17.0.13+11'

To fix this issue, update the **Mule: Home Directory** setting on the new computer to the correct
path for that machine. See Mule: Home Directory.

To prevent this issue when syncing profiles across computers with different usernames, exclude the
`mule.homeDirectory` setting from VS Code settings sync by adding the following to your
`settings.json`:

```json
"settingsSync.ignoredSettings": [
  "mule.homeDirectory"
]
```

### Disable Components to Isolate Issues

When debugging a flow, you can disable (comment out) individual components directly in the canvas.
This allows you to isolate and test parts of your logic without removing or rewriting anything. For
example:

- Temporarily disable a Transform or Logger to test a different path.

- Comment out an entire flow or error handler to simplify the execution logic.

- Disable MUnit test processors to troubleshoot specific assertions.

To disable a component:

Disabled components are unavailable in the canvas and are ignored at runtime. In the code editor,
the block is wrapped in an XML comment.

Once the issue is resolved, you can re-enable the component or use Delete to remove disabled items.

### View Error Messages and Warnings in the Canvas

Anypoint Code Builder shows validation issues directly in the canvas to help you resolve problems
faster. Hover over a component to see a tooltip listing errors and warnings, along with affected
field names.

The configuration sidebar also displays validation messages at the node level.

Field-level errors appear inline during component configuration.

Hover over a component with a red dot to view error details in the canvas.

### Perform a Clean Reinstallation

If you experience persistent issues that other troubleshooting steps don’t resolve, perform a clean
reinstallation of Anypoint Extension Pack:

1.  Close VS Code completely.

2.  Uninstall Anypoint Extension Pack:

    1.  Open VS Code.

    3.  Find and select **Anypoint Extension Pack**.

    5.  Close VS Code.

3.  Delete the `anypoint-code-builder` folder from your user directory:

    - Mac: `~/AnypointCodeBuilder`

    - Windows: `C:\Users\<username>\AnypointCodeBuilder`

4.  Optionally, delete cached extension data from the VS Code extensions folder:

    - Mac: `~/.vscode/extensions/`

    - Windows: `C:\Users\<username>\.vscode\extensions\`

      Remove any folders starting with `salesforce.mule-dx-` or `mulesoftinc.mule-dx-`.

5.  Reopen VS Code and reinstall Anypoint Extension Pack from the Extensions Marketplace.

> [!NOTE] This procedure removes downloaded Mule runtime versions and Java versions. You can
> re-download them after reinstalling.

## Mule Runtime Issues and Errors

Anypoint Code Builder includes bundled Mule runtime versions that enable instant project opening and
design. When you run or debug applications, Anypoint Code Builder checks for the exact runtime
version specified in your project. If the exact version isn’t available locally, error dialogs
appear to help you resolve the issue.

Don’t change the default locations of Mule. If you receive an error that Mule isn’t found or
installed, configure the Mule Home path.

When you configure Mule runtime, ensure you define the `mule.homeDirectory` property.

> [!NOTE] The `mule.runtime.muleRuntimesDirectory` and `mule.runtime.muleHome` properties are legacy
> configurations no longer used.

- **Mule runtime versions**: The Mule runtime versions are located in the `{yourACBHome}/runtimes`
  directory.

  Default value: `/Users/{user}/AnypointCodeBuilder/runtime`.

- **Mule Home**: The full path that points to the root files of the Mule instance.

  Default value: `/Users/<user-name>/AnypointCodeBuilder/runtime/<mule-runtime-installation>`

### Mule Runtime Is Not Installed

The error **Mule Runtime Is Not Installed, You Must Configure a Mule Runtime to Enable This
Feature** occurs if **Mule Home** is misconfigured or empty and a feature requires a running Mule
instance. For example, auto completion and debugging features require Mule to run.

To troubleshoot this issue, use this procedure:

1.  Locate the **Mule > Runtime: Mule Home** property:

2.  Provide the full path to the folder that contains Mule runtime. This field must not be empty.

### No Mule Runtime Found

The warning **No Mule runtime found. To perform this action, you must have Mule runtime
configured.** occurs if:

- Mule isn’t configured properly when you open Anypoint Code Builder

- The **Mule Home** field is misconfigured or empty

To troubleshoot this issue, use this procedure:

2.  Locate the **Mule > Runtime: Mule Home** property:

3.  Provide the full path to the folder that contains Mule runtime. This field must not be empty.

### Please Download and Install a JDK to Compile Your Project

This request is _not_ from MuleSoft or Anypoint Code Builder:

For supported Mule workflows, Anypoint Code Builder resolves Java from the JDK packaged under your
`AnypointCodeBuilder` directory. Using that local JDK source helps avoid machine-specific Java setup
issues and improves project startup reliability.

Instead of using this feature, you can use the command **Download Mule Runtime and Java Versions**.
See Version Settings for Mule, Java, and Connectors.

### Mule Runtime Version Not Defined

The error **Mule runtime version not defined** occurs when your project doesn’t specify a Mule
runtime version in the project’s `mule-artifact.json` file.

To resolve this issue:

2.  In **Project Properties**, select a Mule runtime version.

### Java Version Not Defined

The error **Java version not defined** occurs when your project doesn’t specify a Java version in
the project’s `mule-artifact.json` file.

To resolve this issue:

2.  In **Project Properties**, select a Java version.

### Mule Runtime Version Not Found (Compatible Version Available)

The error **Mule runtime \[version\] not found** occurs when you try to run or debug an application,
but the exact Mule runtime version specified in your project isn’t available locally. However, a
compatible local version is available.

To resolve this issue, you have two options:

- **Continue with compatible version**: Click **Continue** to use the latest local compatible
  version. The dialog shows which version to use.

- **Select a different version**: Click **Open Project Properties** to select a different local Mule
  runtime version or install the exact version using the `MuleSoft: Install Runtime` command.

### Mule Runtime Version Not Found (No Compatible Version)

The error **Mule runtime \[version\] not found** occurs when you try to run or debug an application,
but the exact Mule runtime version specified in your project isn’t available locally, and no
compatible version is available.

To resolve this issue:

2.  In **Project Properties**, either:

    - Use the `MuleSoft: Install Runtime` command to download the required version.

### Java Version Not Found

The error **Java \[version\] not found** occurs when you try to run or debug an application, but the
Java version specified in your project isn’t available locally.

To resolve this issue:

2.  In **Project Properties**, either:

    - Use the `MuleSoft: Download Mule Runtime and Java Versions` command to download the required
      Java version.

### Mule Runtime and Java Version Not Found

The error **Mule runtime \[version\] and Java \[version\] not found** occurs when you try to run or
debug an application, but both the Mule runtime and Java versions specified in your project aren’t
available locally.

To resolve this issue:

2.  In **Project Properties**:

    - Use the `MuleSoft: Install Runtime` command to download the required Mule runtime version, and
      use the `MuleSoft: Download Mule Runtime and Java Versions` command to download the required
      Java version.

### Reinstall Mule Runtime

If your Mule runtime installation becomes corrupted, you can force a reinstallation:

1.  Close Anypoint Code Builder.

3.  Remove or rename the folder for the runtime version you want to reinstall (for example,
    `mule-4.6.0`).

4.  Open Anypoint Code Builder.

> [!NOTE] Your projects and other installed Mule runtime versions are not affected.

## Implementation Errors

You might encounter problems when implementing an API.

### Something Failed While Scaffolding an API

Anypoint Code Builder supports scaffolding these schema fragment files if they’re referenced from
API specs:

|  | Avro | JSON | RAML |
|---|---|---|---|
| **AsyncAPI** | Yes | Yes | No |
| **GraphQL** | No | No | Yes |
| **OData** | No | No | Yes |
| **REST** | No | Yes | Yes |
| **SOAP** | No | No | Yes |

If you add a fragment that isn’t supported, the scaffolder doesn’t add these fragments as project
dependencies when you import the spec from Exchange. However, you can scaffold schemas that are
specified inline within the spec.

If you attempt to scaffold an API that references these types of fragments, you see a message like
the following:

**Something failed while scaffolding API**

The scaffold fails and the flows and other elements aren’t created. To see scaffolding errors,
select **Mule DX Server: Scaffolding** from the list in the output panel.

If you use the iterative approach to scaffold the API (using
multi-root workspaces), the implementation
project folder structure is not created.

To work around this issue, before scaffolding the API:

1.  Add the fragment directly to a folder in your API spec project, such as `fragments`:

2.  Change the path to the fragment from Exchange to the local folder, for example:

    - Reference Local OAS Fragment

    - Reference OAS Fragment on Exchange

    ```YAML
    $ref: fragments/frag-defs.yaml#/components/examples/flightsList
    ```

    ```YAML
    $ref: exchange_modules/e91cab06-650b-4634-9c6f-5bc4f4fc4d17/frag-defs/1.0.0/frag-defs.yaml#/components/examples/flightsList
    ```

3.  Re-scaffold the API.

See
Create and Add a Fragment Directly in Your Spec.

## DataWeave Issues and Errors

When Anypoint Code Builder can’t process a value, it provides a visual indicator to identify an
issue with the value. Issues include:

- Unable to find sample input

- Unable to resolve reference

- Expects _x_ but got _y_

- Invalid input

### Unable to Find Sample Input

The DataWeave error `Unable to find sample input` applies to a Mule event variable, such as
`payload`. In this case, Anypoint Code Builder places a wavy blue line under the value in the
configuration XML file.

If your application isn’t running, Anypoint Code Builder can’t provide any information about Mule
variables unless you provide sample data. Use Quick Fix
to provide sample data in the format and data structure that you expect to be present when the
application runs.

For more information about Mule event variables, see
Predefined Variables.

### Unable to Resolve Reference

The error `Unable to resolve reference` is typically for a sequence of characters like `afkdldjf`
that isn’t recognized.

Either provide the intended value or use Quick Fix to
convert the character sequence into a DataWeave variable. For more information, see
DataWeave Variables.

### Expects _x_ but Got _y_

The error similar to `Expects _x_ but got _y_` typically indicates that something is wrong with the
provided function. For example, `Expects 1 argument but got 0` occurs for `round()` because the
function is missing an argument, in this case, a number to round. An example of a fix is
`round(1.65)`. Similar errors indicate that an argument is of the wrong data type or that a function
is otherwise malformed and requires correction.

Read the error message to determine what part of the expression to fix, and review the function
description after the error message to learn more about the function. See
DataWeave Modules to find additional DataWeave
function documentation.

### Invalid Input

The error `Invalid input` typically occurs when special characters, such as `?`, appear in a
DataWeave expression and aren’t escaped, for example:

For more information, see
Rules for Declaring Valid Identifiers
and
Escape Special Characters.

## Project Loading Errors

Errors sometimes occur when you open or start a project in Anypoint Code Builder.

### Loading Error in the Canvas

A **Loading…​** error in the graphical UI (canvas) often occurs under these conditions:

- When importing a project due to a missing dependency

To check for a missing dependency:

3.  Search for an error caused by the missing dependency, similar to this one:

    Caused by: org.eclipse.aether.transfer.ArtifactNotFoundException: Failure to find
    org.mule.examples:accelerator-common-config-module:jar:mule-plugin:1.1.0 in
    https://repo.maven.apache.org/maven2/ was cached in the local repository, resolution will not be
    reattempted until the update interval of central has elapsed or updates are forced

4.  If you find a missing dependency, log in to Anypoint Platform.

    The canvas loads after all dependencies load.

    When a browser extension is interfering with the UI loading process, you see:

To address this issue, try:

- Disabling browser extensions and reloading the application

- Using another browser that is not using extensions

### UI Canvas Renders Without Configured Flows or Subflows

If the UI for an application that is already configured with a flow or subflow treats your
application as a new project, prompting you with the question **How do you want to start building
your project?** and **Build a flow** and **Build a sub flow** creation options, make sure that your
application is open from its _root_ directory or from a multi-root workspace.

Visual Studio Code treats an open directory as a workspace. For the project to load into a
workspace, the root directory of the project must be the top-level directory in the Explorer view,
or the project must belong to a
[multi-root workspace](https://code.visualstudio.com/docs/editing/workspaces/multi-root-workspaces).

2.  Provide this command:

    ```command
    File: Open Folder...
    ```

See also Importing Projects into Anypoint Code Builder and
Working with Workspaces.

### Mule DX API Component Was Not Installed

The error indicates that some Anypoint Code Builder dependencies have not finished loading. This
issue typically occurs when you click **Design an API** and is often accompanied by the notification
**Extracting Mule runtime: This operation may take a while…​**. The extraction process can take
several minutes, particularly after you install or update Anypoint Extension Pack.

1.  Wait for the error **Mule DX API Component was not installed** to disappear.

2.  Retry your action.

To monitor the progress of backend processes:

### Dependency Resolution Error

The error `There was an issue solving the dependencies for the asset` occurs when a dependency is
missing. Usually, the appears after you import or open an integration or implementation project that
is missing one or more dependencies for a connector operation.

To address this issue and avoid other errors, try logging in to Anypoint Platform, and wait for the
project to finish loading before attempting to resolve any missing dependencies that remain.

## Deployment Errors

In Anypoint Code Builder, the error `Failed to deploy to CloudHub: 400` occurs when you deploy a
Mule application to CloudHub if the root organization or business group to which you are deploying
lacks a sufficient vCore allocation.

To address this isssue, increase the vCore allocation to the root organization or business group in
the **Sandbox** environment:

- To reallocate resources, see
  Redistribute Resources Between Existing Business Groups.

- To manage environments, see Anypoint Platform Environments.
  For additional help, contact your organization administrator for Anypoint Platform.

## Authentication Errors

Authentication errors sometimes occur when you attempt to perform actions that require a connection
to Anypoint Platform or to services that Anypoint Code Builder relies on.

### Failed to Authenticate to Git

All commands that involve `git` actions, such as publishing to Exchange and committing changes to an
API specification, require authentication with the correct Anypoint Platform host cloud. If
authentication fails, the action throws this VS Code error:

Failed to authenticate to git remote

To address this issue, cancel the error notification, and ensure that Anypoint Code Builder is set
to the correct region for your project and that you are logged in to Anypoint Platform.

## Missing or Disabled Features

Some Anypoint Code Builder features can be disabled or hidden based on your settings.

For any features that aren’t working as expected, first
check for problems and issues.

### MuleSoft Icon Missing from the Activity Bar

If the MuleSoft icon (see Discovering the UI) is missing from the Activity Bar,
check for and address common causes.

- Enable Anypoint Code Builder in the Activity Bar

- Check for Restricted Mode

- Modify Trust Settings

#### Enable Anypoint Code Builder in the Activity Bar

Use the Activity Bar to enable or disable icons.

2.  Check for **Anypoint Code Builder**:

    - If **Anypoint Code Builder** is disabled, click **Anypoint Code Builder** to add the icon to
      the Activity Bar.

    - If **Anypoint Code Builder** is not present, see
      Check for Anypoint Extension Pack Installation. If the
      Anypoint Extension Pack is installed, Check for Restricted Mode.

#### Check for Restricted Mode

If your project or workspace is in restricted mode, the MuleSoft icon does not appear in the
Activity Bar.

To determine whether your project or workspace is trusted or in restricted mode:

2.  Provide the following command to launch the **Workspace Trust** tab:

    ```command
    Workspace: Manage Workspace Trust
    ```

    If the **Workspace Trust** tab says **You are in Restricted Mode**, you can click **Trust** or
    **Trust Parent**.

3.  After trusting, check for the MuleSoft icon in the Activity Bar.

For more information about trust settings, see
[Trusting a workspace](https://code.visualstudio.com/docs/editing/workspaces/workspace-trust) in the
VS Code documentation.

#### Modify Trust Settings

To modify your trust settings:

1.  Provide the following command to launch the **Workspace Trust** tab:

    ```command
    Workspace: Configure Workspace Trust Settings
    ```

2.  Review and adjust the workspace settings, as needed.

### Incomplete Flow or Corrupted XML

If a flow lacks a component or contains only a trigger, such as an HTTP Listener operation or the
Scheduler, an error similar to the following appears in the **Problems** panel and from the code
editor:

The content of element 'flow' is not complete. One of
'{"http://www.mulesoft.org/schema/mule/core":abstract-message-processor,
"http://www.mulesoft.org/schema/mule/core":abstract-mixed-content-message-processor}' is
expected.(cvc-complex-type.2.4.b)

To address this issue, add processing components or connector operations to your flow, such as a
Logger or HTTP Request operation. For reference documentation on specific connector and component
configurations, see Anypoint Code Builder Components and Commands Reference.

This error can also occur if XML tags in the configuration file are corrupted or not properly
closed. If you’ve already added components and the error persists, check the configuration XML for
unclosed tags. To prevent XML corruption, save your work frequently and use source control
management (SCM) to back up your projects.

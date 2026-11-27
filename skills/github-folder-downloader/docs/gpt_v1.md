# **Plan: Robust GitHub Folder Downloader & Mirror**

## **1. Objective**

Create a production-quality Python CLI utility that accepts two required command-line parameters:

1. **GitHub repository folder URL** — the URL pointing to a specific folder inside a GitHub repository.
2. **Local destination directory** — the directory into which the folder's content should be downloaded and mirrored.

The script should retrieve the contents of a GitHub folder, preserve its folder/file structure as closely as practical, and handle download failures and extraction failures gracefully.

**Primary goal:** Download a specific GitHub repository subdirectory, not unnecessarily download the entire repository when a more targeted method is available.

**Fallback goal:** If the folder cannot be retrieved or reconstructed reliably through the primary method, download the repository archive, retain the archive in the destination directory, and attempt safe extraction. If extraction fails, preserve the downloaded archive for manual recovery.

## **2. Proposed command-line interface**

The script should be executable from a terminal with two positional arguments.

```
python github_folder_downloader.py \
    "https://github.com/OWNER/REPO/tree/BRANCH/PATH/TO/FOLDER" \
    "/path/to/local/destination"
```

**Example:**

```
python github_folder_downloader.py \
    "https://github.com/nordeim/my-pi-agent/tree/main/skills/solving-a-level-exam-papers" \
    "/tmp/skill"
```

The example above illustrates the CLI format, not a verified download or an assertion about the repository's current contents.

### **Input contract**

| Parameter           | Required | Description                                                               |
| ------------------- | -------- | ------------------------------------------------------------------------- |
| `github_folder_url` | Yes      | GitHub URL pointing to a folder inside a repository.                      |
| `destination`       | Yes      | Local destination directory where the folder's contents will be mirrored. |

The script should accept URLs in the following general format:

```
https://github.com/OWNER/REPO/tree/BRANCH/SUBDIRECTORY
```

It should also ideally support branches whose names contain slashes, such as:

```
feature/new-solver
```

This requires careful URL parsing because the branch name and repository subdirectory are both represented in the URL path.

## **3. Retrieval strategy**

**The script should use a layered retrieval strategy instead of relying on one download method.**

**Tier 1 — GitHub API retrieval**

Preferred method

Retrieve the target directory and its files without downloading unrelated repository content.

**Tier 2 — Repository archive fallback**

Fallback method

Download the repository archive and extract only the requested directory, preserving its relative structure.

**Tier 3 — Preserve the archive**

Recovery mechanism

If safe extraction cannot complete, preserve the archive in the destination directory and report the failure.

### **Tier 1 — GitHub API retrieval**

The preferred method should retrieve the folder contents through GitHub's API or GitHub's raw-content service.

The implementation should use a structured retrieval approach:

1. Resolve the repository owner and name.
2. Resolve the branch or Git ref.
3. Resolve the target directory within the repository.
4. Retrieve the directory's file tree.
5. Download the files individually.
6. Reconstruct the directory locally.

This approach avoids downloading unrelated files from the repository.

#### **Proposed API approach**

Use GitHub's repository tree API to retrieve the relevant tree metadata when practical.

The implementation should evaluate whether to use:

- The Git Trees API.
- The Contents API.
- Raw file URLs.

**Recommended combination:**

- Git Trees API for file and directory discovery, where its response is usable.
- Raw file downloads for downloading individual files.
- Contents API or non-recursive tree requests as a fallback if tree retrieval is incomplete or truncated.

This avoids unnecessary API calls while preserving the ability to handle large or unusual repository structures.

### **Expected local directory layout**

Suppose the user supplies:

```
https://github.com/OWNER/REPO/tree/main/skills/my-skill
```

And the destination:

```
/tmp/downloaded-skill
```

Suppose the GitHub source contains:

```
skills/my-skill/
├── SKILL.md
├── README.md
├── references/
│   ├── guide.md
│   └── examples.md
├── scripts/
│   └── helper.py
└── assets/
    └── template.json
```

**The preferred result should be:**

```
/tmp/downloaded-skill/
├── SKILL.md
├── README.md
├── references/
│   ├── guide.md
│   └── examples.md
├── scripts/
│   └── helper.py
└── assets/
    └── template.json
```

**The destination directory should contain the contents of the requested GitHub folder, rather than automatically nesting the entire repository structure.**

This is more convenient for downloading standalone skills, templates, examples, or other reusable subdirectories.

The implementation should preserve:

- Relative file paths.
- Nested subdirectories.
- File names.
- File contents.
- Empty directories, where the GitHub representation permits their discovery.

GitHub itself does not track empty directories in Git, so empty directories that do not contain tracked entries cannot reliably be reconstructed.

## **4. Input URL parsing and branch resolution**

This is one of the most important parts of the design.

### **Supported input formats**

The initial implementation should support:

| URL type                                           | Support                         |
| -------------------------------------------------- | ------------------------------- |
| GitHub folder URL using `tree`                     | Required                        |
| GitHub folder URL with normal branch names         | Required                        |
| GitHub folder URL with branch names containing `/` | Required, subject to resolution |
| GitHub folder URL with URL-encoded components      | Required                        |
| GitHub folder URL with a tag or commit ref         | Recommended                     |
| GitHub repository root URL                         | Recommended                     |
| GitHub `blob` file URL                             | Not in initial scope            |
| GitHub Gist                                        | Not in initial scope            |
| GitLab / Bitbucket URLs                            | Not in initial scope            |

### **Branch names containing slashes**

Consider this URL:

```
https://github.com/OWNER/REPO/tree/feature/new-solver/skills/math
```

The URL path does not inherently distinguish whether:

```
feature/new-solver
```

is the branch, or whether:

```
feature
```

is the branch and `new-solver/skills/math` is the directory.

The script should not assume that the first segment following `tree` is always the branch name.

**Proposed resolution strategy:**

1. Extract the owner and repository.
2. Extract the remaining URL path after the `tree` component.
3. Generate candidate ref prefixes, from longest to shortest.
4. Verify candidate refs using GitHub's API.
5. Determine the remaining path after the verified ref.
6. Confirm that the remaining path resolves to a directory.
7. If the ref or directory cannot be resolved unambiguously, report the ambiguity or use a carefully controlled resolution fallback.

**Important limitation:** A branch name and a folder path can overlap. Automated resolution may be ambiguous. The script must not silently select an arbitrary interpretation if it cannot reliably identify the requested directory.

The implementation should handle URL encoding and API URL encoding correctly, rather than simply concatenating untrusted URL components.

## **5. Tier 2 — Repository archive fallback**

If the targeted retrieval method fails, the script should attempt a repository archive download.

### **Archive formats**

The fallback should support at least:

- **ZIP archive** — recommended first choice.
- **TAR.GZ archive** — optional alternative if ZIP retrieval or processing fails.

The GitHub archive service can provide an archive of a repository at a specified ref.

**The archive contains the entire repository, not just the requested subdirectory.**

The script therefore must identify the requested directory within the downloaded archive and extract only the requested directory's contents.

### **Proposed fallback sequence**

\#chatgpt-mermaid-\_r_19o\_{font-family:-apple-system-body,ui-sans-serif,-apple-system,system-ui,"Segoe UI",Helvetica,"Apple Color Emoji",Arial,sans-serif,"Segoe UI Emoji","Segoe UI Symbol";font-size:16px;fill:rgb(13, 13, 13);}@keyframes edge-animation-frame{from{stroke-dashoffset:0;}}@keyframes dash{to{stroke-dashoffset:0;}}#chatgpt-mermaid-\_r_19o\_ .edge-animation-slow{stroke-dasharray:9,5!important;stroke-dashoffset:900;animation:dash 50s linear infinite;stroke-linecap:round;}#chatgpt-mermaid-\_r_19o\_ .edge-animation-fast{stroke-dasharray:9,5!important;stroke-dashoffset:900;animation:dash 20s linear infinite;stroke-linecap:round;}#chatgpt-mermaid-\_r_19o\_ .error-icon{fill:rgb(243, 243, 243);}#chatgpt-mermaid-\_r_19o\_ .error-text{fill:rgb(13, 13, 13);stroke:rgb(13, 13, 13);}#chatgpt-mermaid-\_r_19o\_ .edge-thickness-normal{stroke-width:1px;}#chatgpt-mermaid-\_r_19o\_ .edge-thickness-thick{stroke-width:3.5px;}#chatgpt-mermaid-\_r_19o\_ .edge-pattern-solid{stroke-dasharray:0;}#chatgpt-mermaid-\_r_19o\_ .edge-thickness-invisible{stroke-width:0;fill:none;}#chatgpt-mermaid-\_r_19o\_ .edge-pattern-dashed{stroke-dasharray:3;}#chatgpt-mermaid-\_r_19o\_ .edge-pattern-dotted{stroke-dasharray:2;}#chatgpt-mermaid-\_r_19o\_ .marker{fill:rgb(143, 143, 143);stroke:rgb(143, 143, 143);}#chatgpt-mermaid-\_r_19o\_ .marker.cross{stroke:rgb(143, 143, 143);}#chatgpt-mermaid-\_r_19o\_ svg{font-family:-apple-system-body,ui-sans-serif,-apple-system,system-ui,"Segoe UI",Helvetica,"Apple Color Emoji",Arial,sans-serif,"Segoe UI Emoji","Segoe UI Symbol";font-size:16px;}#chatgpt-mermaid-\_r_19o\_ p{margin:0;}#chatgpt-mermaid-\_r_19o\_ .label{font-family:-apple-system-body,ui-sans-serif,-apple-system,system-ui,"Segoe UI",Helvetica,"Apple Color Emoji",Arial,sans-serif,"Segoe UI Emoji","Segoe UI Symbol";color:rgb(13, 13, 13);}#chatgpt-mermaid-\_r_19o\_ .cluster-label text{fill:rgb(13, 13, 13);}#chatgpt-mermaid-\_r_19o\_ .cluster-label span{color:rgb(13, 13, 13);}#chatgpt-mermaid-\_r_19o\_ .cluster-label span p{background-color:transparent;}#chatgpt-mermaid-\_r_19o\_ .label text,#chatgpt-mermaid-\_r_19o\_ span{fill:rgb(13, 13, 13);color:rgb(13, 13, 13);}#chatgpt-mermaid-\_r_19o\_ .node rect,#chatgpt-mermaid-\_r_19o\_ .node circle,#chatgpt-mermaid-\_r_19o\_ .node ellipse,#chatgpt-mermaid-\_r_19o\_ .node polygon,#chatgpt-mermaid-\_r_19o\_ .node path{fill:rgb(222, 234, 251);stroke:rgb(83, 154, 248);stroke-width:1px;}#chatgpt-mermaid-\_r_19o\_ .rough-node .label text,#chatgpt-mermaid-\_r_19o\_ .node .label text,#chatgpt-mermaid-\_r_19o\_ .image-shape .label,#chatgpt-mermaid-\_r_19o\_ .icon-shape .label{text-anchor:middle;}#chatgpt-mermaid-\_r_19o\_ .node .katex path{fill:#000;stroke:#000;stroke-width:1px;}#chatgpt-mermaid-\_r_19o\_ .rough-node .label,#chatgpt-mermaid-\_r_19o\_ .node .label,#chatgpt-mermaid-\_r_19o\_ .image-shape .label,#chatgpt-mermaid-\_r_19o\_ .icon-shape .label{text-align:center;}#chatgpt-mermaid-\_r_19o\_ .node.clickable{cursor:pointer;}#chatgpt-mermaid-\_r_19o\_ .root .anchor path{fill:rgb(143, 143, 143)!important;stroke-width:0;stroke:rgb(143, 143, 143);}#chatgpt-mermaid-\_r_19o\_ .arrowheadPath{fill:rgb(143, 143, 143);}#chatgpt-mermaid-\_r_19o\_ .edgePath .path{stroke:rgb(143, 143, 143);stroke-width:1px;}#chatgpt-mermaid-\_r_19o\_ .flowchart-link{stroke:rgb(143, 143, 143);fill:none;}#chatgpt-mermaid-\_r_19o\_ .edgeLabel{background-color:rgb(252, 252, 252);text-align:center;}#chatgpt-mermaid-\_r_19o\_ .edgeLabel p{background-color:rgb(252, 252, 252);}#chatgpt-mermaid-\_r_19o\_ .edgeLabel rect{opacity:0.5;background-color:rgb(252, 252, 252);fill:rgb(252, 252, 252);}#chatgpt-mermaid-\_r_19o\_ .labelBkg{background-color:rgba(252, 252, 252, 0.5);}#chatgpt-mermaid-\_r_19o\_ .cluster rect{fill:rgb(243, 243, 243);stroke:rgba(0, 0, 0, 0.1);stroke-width:1px;}#chatgpt-mermaid-\_r_19o\_ .cluster text{fill:rgb(13, 13, 13);}#chatgpt-mermaid-\_r_19o\_ .cluster span{color:rgb(13, 13, 13);}#chatgpt-mermaid-\_r_19o\_ div.mermaidTooltip{position:absolute;text-align:center;max-width:200px;padding:2px;font-family:-apple-system-body,ui-sans-serif,-apple-system,system-ui,"Segoe UI",Helvetica,"Apple Color Emoji",Arial,sans-serif,"Segoe UI Emoji","Segoe UI Symbol";font-size:12px;background:rgb(243, 243, 243);border:1px solid rgba(0, 0, 0, 0.1);border-radius:2px;pointer-events:none;z-index:100;}#chatgpt-mermaid-\_r_19o\_ .flowchartTitleText{text-anchor:middle;font-size:18px;fill:rgb(13, 13, 13);}#chatgpt-mermaid-\_r_19o\_ rect.text{fill:none;stroke-width:0;}#chatgpt-mermaid-\_r_19o\_ .icon-shape,#chatgpt-mermaid-\_r_19o\_ .image-shape{background-color:rgb(252, 252, 252);text-align:center;}#chatgpt-mermaid-\_r_19o\_ .icon-shape p,#chatgpt-mermaid-\_r_19o\_ .image-shape p{background-color:rgb(252, 252, 252);padding:2px;}#chatgpt-mermaid-\_r_19o\_ .icon-shape .label rect,#chatgpt-mermaid-\_r_19o\_ .image-shape .label rect{opacity:0.5;background-color:rgb(252, 252, 252);fill:rgb(252, 252, 252);}#chatgpt-mermaid-\_r_19o\_ .label-icon{display:inline-block;height:1em;overflow:visible;vertical-align:-0.125em;}#chatgpt-mermaid-\_r_19o\_ .node .label-icon path{fill:currentColor;stroke:revert;stroke-width:revert;}#chatgpt-mermaid-\_r_19o\_ .node .neo-node{stroke:rgb(83, 154, 248);}#chatgpt-mermaid-\_r_19o\_ [data-look="neo"].node rect,#chatgpt-mermaid-\_r_19o\_ [data-look="neo"].cluster rect,#chatgpt-mermaid-\_r_19o\_ [data-look="neo"].node polygon{stroke:url(#chatgpt-mermaid-\_r_19o\_-gradient);filter:drop-shadow( 1px 2px 2px rgba(185,185,185,1));}#chatgpt-mermaid-\_r_19o\_ [data-look="neo"].swimlane.cluster rect{filter:none;}#chatgpt-mermaid-\_r_19o\_ [data-look="neo"].node path{stroke:url(#chatgpt-mermaid-\_r_19o\_-gradient);stroke-width:1px;}#chatgpt-mermaid-\_r_19o\_ [data-look="neo"].node .outer-path{filter:drop-shadow( 1px 2px 2px rgba(185,185,185,1));}#chatgpt-mermaid-\_r_19o\_ [data-look="neo"].node .neo-line path{stroke:rgb(83, 154, 248);filter:none;}#chatgpt-mermaid-\_r_19o\_ [data-look="neo"].node circle{stroke:url(#chatgpt-mermaid-\_r_19o\_-gradient);filter:drop-shadow( 1px 2px 2px rgba(185,185,185,1));}#chatgpt-mermaid-\_r_19o\_ [data-look="neo"].node circle .state-start{fill:#000000;}#chatgpt-mermaid-\_r_19o\_ [data-look="neo"].icon-shape .icon{fill:url(#chatgpt-mermaid-\_r_19o\_-gradient);filter:drop-shadow( 1px 2px 2px rgba(185,185,185,1));}#chatgpt-mermaid-\_r_19o\_ [data-look="neo"].icon-shape .icon-neo path{stroke:url(#chatgpt-mermaid-\_r_19o\_-gradient);filter:drop-shadow( 1px 2px 2px rgba(185,185,185,1));}#chatgpt-mermaid-\_r_19o\_ .node text{font-size:14px;font-weight:600;letter-spacing:normal;fill:rgb(0, 79, 153);}#chatgpt-mermaid-\_r_19o\_ .edgeLabels text{font-size:13px;font-weight:600;letter-spacing:-0.08px;fill:rgb(0, 79, 153);}#chatgpt-mermaid-\_r_19o\_ .node tspan[font-weight="normal"],#chatgpt-mermaid-\_r_19o\_ .edgeLabels tspan[font-weight="normal"]{font-weight:600;}#chatgpt-mermaid-\_r_19o\_ .edgeLabel .label rect{opacity:1;rx:13px;ry:13px;fill:rgb(245, 250, 255);stroke:rgb(206, 219, 229);stroke-width:1px;}#chatgpt-mermaid-\_r_19o\_ .node rect,#chatgpt-mermaid-\_r_19o\_ .node circle,#chatgpt-mermaid-\_r_19o\_ .node ellipse,#chatgpt-mermaid-\_r_19o\_ .node polygon,#chatgpt-mermaid-\_r_19o\_ .node path{fill:rgb(229, 243, 255);stroke:rgba(0, 0, 0, 0.1);stroke-width:1px;}#chatgpt-mermaid-\_r_19o\_ .node rect{rx:16px;ry:16px;}#chatgpt-mermaid-\_r_19o\_ .mermaid-decision .label-container{fill:rgb(245, 250, 255);stroke:rgb(206, 219, 229);stroke-dasharray:2,2;}#chatgpt-mermaid-\_r_19o\_ .edgePaths .flowchart-link{stroke:rgb(143, 143, 143);stroke-width:1px;stroke-linecap:round;stroke-linejoin:round;}#chatgpt-mermaid-\_r_19o\_ .marker{fill:rgb(143, 143, 143);stroke:rgb(143, 143, 143);}#chatgpt-mermaid-\_r_19o\_ :root{--mermaid-font-family:-apple-system-body,ui-sans-serif,-apple-system,system-ui,"Segoe UI",Helvetica,"Apple Color Emoji",Arial,sans-serif,"Segoe UI Emoji","Segoe UI Symbol";}Primary API retrieval failsDownload repository ZIPZIP download successful?Validate archiveTry TAR.GZ fallbackTAR.GZ download successful?Validate archiveReport retrieval failureExtract target folder safelyExtraction successful?Commit files to destinationPreserve archive in destinationReport extraction failureYesNoYesNoYesNo

### **Archive processing**

The script should:

1. Download the archive to a temporary location.
2. Verify that the downloaded file is within configured size limits.
3. Validate the archive format.
4. Identify the repository's archive root directory.
5. Locate the requested directory relative to that archive root.
6. Extract only the requested directory's contents.
7. Preserve the requested directory's internal structure.
8. Verify the extraction results.
9. Move the extracted files into the destination.
10. Delete the temporary archive after successful extraction and commit, unless an optional retention setting is enabled.

### **Archive retention policy**

**Default behavior:**

| Situation                                         | Archive handling                       |
| ------------------------------------------------- | -------------------------------------- |
| Primary API retrieval succeeds                    | No archive downloaded                  |
| Archive downloaded and target extraction succeeds | Archive removed from temporary storage |
| Archive download succeeds but extraction fails    | Preserve archive in destination        |
| Archive download fails                            | Report the failure                     |
| ZIP fallback fails and TAR.GZ succeeds            | Process TAR.GZ                         |
| Both archive methods fail                         | Report all relevant failures           |

The retained archive should have an informative filename, such as:

```
/tmp/downloaded-skill/
└── my-pi-agent-main.zip
```

Or:

```
/tmp/downloaded-skill/
└── my-pi-agent-main.tar.gz
```

**The archive should be preserved in its original downloaded format, not converted or re-compressed.**

If extraction fails, the script should preserve the archive bytes as downloaded, rather than modifying the archive during recovery.

## **6. Extraction safety and security**

The archive fallback introduces risks that the original direct-file downloader did not have. The improved implementation should treat archive contents as untrusted input.

### **A. Path traversal protection**

The script must reject archive entries that attempt to escape the extraction directory.

For example, paths resembling:

```
../../outside.txt
```

or paths containing absolute paths should not be allowed to write outside the intended extraction boundary.

The implementation should validate resolved paths and ensure they remain within the staging directory.

### **B. ZIP archive protections**

The script should guard against:

- ZIP path traversal.
- Unexpected absolute paths.
- Excessive archive sizes.
- Excessive numbers of entries.
- Excessive total extracted size.
- Excessive individual file sizes.
- Suspicious compression ratios.
- Symlinks or special entries.
- Unexpected directory structures.

### **C. TAR.GZ protections**

The script should guard against:

- Path traversal.
- Absolute paths.
- Symbolic links.
- Hard links.
- Device entries.
- FIFOs.
- Other non-regular file types.
- Excessive extracted sizes.
- Excessive numbers of entries.

**The script should extract only ordinary files and directories.**

It should not restore executable permissions or other potentially dangerous metadata from archive entries unless there is an explicit, carefully justified requirement.

### **D. Archive extraction should not execute anything**

The downloader should never:

- Execute extracted scripts.
- Import extracted Python modules.
- Run shell commands from repository contents.
- Invoke package installation commands.
- Automatically launch applications.
- Run Git hooks.
- Execute build scripts.

**The downloader's job is to retrieve and reconstruct files, not to execute the repository.**

## **7. Destination directory handling**

The destination directory is the second positional input.

The implementation should carefully define how it behaves if the directory already exists.

### **Recommended behavior**

| Condition                                       | Behavior                                              |
| ----------------------------------------------- | ----------------------------------------------------- |
| Destination does not exist                      | Create it.                                            |
| Destination already exists and is a directory   | Reuse it.                                             |
| Destination already contains unrelated files    | Preserve them.                                        |
| Downloaded file conflicts with an existing file | Replace only after successful staging and validation. |
| Destination path is a regular file              | Abort with a clear error.                             |
| Destination is inaccessible                     | Report a clear permission error.                      |
| Disk space is insufficient                      | Report failure and clean up temporary files.          |

**Recommended implementation:** Use a staging directory inside the destination or a suitable temporary directory, then commit validated files into the destination only after the download and reconstruction have succeeded.

This minimizes the risk of leaving the destination in a partially reconstructed state.

### **Overwrite policy**

The script should not delete the destination directory.

Instead:

- Preserve unrelated existing files.
- Replace conflicting files only when the new download has been successfully staged.
- Report any conflicts or failures.
- Avoid unnecessary destructive cleanup.

**Note:** A fully atomic replacement of an entire directory tree is not straightforward when merging with an existing destination. The implementation should aim for transactional staging and controlled replacement of individual files, with clear reporting if the commit is interrupted.

## **8. CLI design and user experience**

The script should use Python's built-in `argparse` rather than manually parsing `sys.argv`.

### **Required positional arguments**

```
github_folder_url
destination
```

### **Optional arguments worth implementing**

| Argument               | Default        | Purpose                                                     |
| ---------------------- | -------------- | ----------------------------------------------------------- |
| `--timeout`            | 30 seconds     | HTTP operation timeout                                      |
| `--max-download-size`  | 100 MiB        | Maximum permitted download size                             |
| `--max-extracted-size` | 250 MiB        | Maximum permitted reconstructed content size                |
| `--max-files`          | 5,000          | Maximum permitted file count                                |
| `--max-depth`          | 100            | Maximum directory nesting depth                             |
| `--keep-archive`       | False          | Retain downloaded archive even when extraction succeeds     |
| `--verbose`            | False          | Enable more detailed diagnostics                            |
| `--no-overwrite`       | False          | Refuse to replace conflicting destination files             |
| `--token-env`          | `GITHUB_TOKEN` | Optional environment variable containing a GitHub API token |

These are proposed defaults for the blueprint, not validated universal limits. They should be configurable and documented.

The script should remain easy to use with only the two mandatory arguments.

Example:

```
python github_folder_downloader.py \
  "https://github.com/OWNER/REPO/tree/main/path/to/folder" \
  "/tmp/download"
```

Optional advanced usage:

```
python github_folder_downloader.py \
  "https://github.com/OWNER/REPO/tree/main/path/to/folder" \
  "/tmp/download" \
  --timeout 45 \
  --max-download-size 200 \
  --max-extracted-size 500 \
  --verbose
```

**The size arguments in this example should be interpreted consistently, preferably as MiB, with that unit clearly documented.**

## **9. HTTP implementation requirements**

The implementation should use Python's standard library where possible.

### **Recommended standard-library components**

| Component        | Purpose                                         |
| ---------------- | ----------------------------------------------- |
| `argparse`       | CLI arguments                                   |
| `urllib.request` | HTTP requests                                   |
| `urllib.parse`   | URL parsing and encoding                        |
| `pathlib`        | Filesystem paths                                |
| `tempfile`       | Temporary download and staging files            |
| `zipfile`        | ZIP archive validation and processing           |
| `tarfile`        | TAR.GZ archive validation and processing        |
| `hashlib`        | File hashing                                    |
| `json`           | GitHub API response parsing                     |
| `logging`        | Diagnostics                                     |
| `shutil`         | Filesystem operations                           |
| `os`             | Filesystem operations and environment variables |
| `stat`           | File type validation                            |
| `time`           | Retry/backoff timing, if required               |

### **HTTP requirements**

The HTTP layer should implement:

- HTTPS-only URLs.
- Appropriate `User-Agent`.
- Accept headers appropriate to GitHub APIs.
- Explicit timeouts.
- Response-size limits.
- Streaming downloads instead of unbounded `read()`.
- Clear HTTP error reporting.
- Limited retry handling for transient failures.
- Backoff for HTTP 429 and transient server errors.
- Respect for `Retry-After`, when provided.
- Proper resource closure.
- Optional GitHub authentication through an environment variable.
- No exposure of credentials in log messages.

### **Authentication**

The script should work without a GitHub token for public repositories where API and download access permits.

An optional GitHub token may be used for:

- Higher API rate limits.
- Access to private repositories, if the token is authorized.
- Better reliability for automated use.

The token should be obtained from an environment variable rather than embedded in the source code or command-line arguments.

## **10. Proposed architecture**

I recommend separating the implementation into logical functions, even if the deliverable remains a single Python file.

\#chatgpt-mermaid-\_r_1aj\_{font-family:-apple-system-body,ui-sans-serif,-apple-system,system-ui,"Segoe UI",Helvetica,"Apple Color Emoji",Arial,sans-serif,"Segoe UI Emoji","Segoe UI Symbol";font-size:16px;fill:rgb(13, 13, 13);}@keyframes edge-animation-frame{from{stroke-dashoffset:0;}}@keyframes dash{to{stroke-dashoffset:0;}}#chatgpt-mermaid-\_r_1aj\_ .edge-animation-slow{stroke-dasharray:9,5!important;stroke-dashoffset:900;animation:dash 50s linear infinite;stroke-linecap:round;}#chatgpt-mermaid-\_r_1aj\_ .edge-animation-fast{stroke-dasharray:9,5!important;stroke-dashoffset:900;animation:dash 20s linear infinite;stroke-linecap:round;}#chatgpt-mermaid-\_r_1aj\_ .error-icon{fill:rgb(243, 243, 243);}#chatgpt-mermaid-\_r_1aj\_ .error-text{fill:rgb(13, 13, 13);stroke:rgb(13, 13, 13);}#chatgpt-mermaid-\_r_1aj\_ .edge-thickness-normal{stroke-width:1px;}#chatgpt-mermaid-\_r_1aj\_ .edge-thickness-thick{stroke-width:3.5px;}#chatgpt-mermaid-\_r_1aj\_ .edge-pattern-solid{stroke-dasharray:0;}#chatgpt-mermaid-\_r_1aj\_ .edge-thickness-invisible{stroke-width:0;fill:none;}#chatgpt-mermaid-\_r_1aj\_ .edge-pattern-dashed{stroke-dasharray:3;}#chatgpt-mermaid-\_r_1aj\_ .edge-pattern-dotted{stroke-dasharray:2;}#chatgpt-mermaid-\_r_1aj\_ .marker{fill:rgb(143, 143, 143);stroke:rgb(143, 143, 143);}#chatgpt-mermaid-\_r_1aj\_ .marker.cross{stroke:rgb(143, 143, 143);}#chatgpt-mermaid-\_r_1aj\_ svg{font-family:-apple-system-body,ui-sans-serif,-apple-system,system-ui,"Segoe UI",Helvetica,"Apple Color Emoji",Arial,sans-serif,"Segoe UI Emoji","Segoe UI Symbol";font-size:16px;}#chatgpt-mermaid-\_r_1aj\_ p{margin:0;}#chatgpt-mermaid-\_r_1aj\_ .label{font-family:-apple-system-body,ui-sans-serif,-apple-system,system-ui,"Segoe UI",Helvetica,"Apple Color Emoji",Arial,sans-serif,"Segoe UI Emoji","Segoe UI Symbol";color:rgb(13, 13, 13);}#chatgpt-mermaid-\_r_1aj\_ .cluster-label text{fill:rgb(13, 13, 13);}#chatgpt-mermaid-\_r_1aj\_ .cluster-label span{color:rgb(13, 13, 13);}#chatgpt-mermaid-\_r_1aj\_ .cluster-label span p{background-color:transparent;}#chatgpt-mermaid-\_r_1aj\_ .label text,#chatgpt-mermaid-\_r_1aj\_ span{fill:rgb(13, 13, 13);color:rgb(13, 13, 13);}#chatgpt-mermaid-\_r_1aj\_ .node rect,#chatgpt-mermaid-\_r_1aj\_ .node circle,#chatgpt-mermaid-\_r_1aj\_ .node ellipse,#chatgpt-mermaid-\_r_1aj\_ .node polygon,#chatgpt-mermaid-\_r_1aj\_ .node path{fill:rgb(222, 234, 251);stroke:rgb(83, 154, 248);stroke-width:1px;}#chatgpt-mermaid-\_r_1aj\_ .rough-node .label text,#chatgpt-mermaid-\_r_1aj\_ .node .label text,#chatgpt-mermaid-\_r_1aj\_ .image-shape .label,#chatgpt-mermaid-\_r_1aj\_ .icon-shape .label{text-anchor:middle;}#chatgpt-mermaid-\_r_1aj\_ .node .katex path{fill:#000;stroke:#000;stroke-width:1px;}#chatgpt-mermaid-\_r_1aj\_ .rough-node .label,#chatgpt-mermaid-\_r_1aj\_ .node .label,#chatgpt-mermaid-\_r_1aj\_ .image-shape .label,#chatgpt-mermaid-\_r_1aj\_ .icon-shape .label{text-align:center;}#chatgpt-mermaid-\_r_1aj\_ .node.clickable{cursor:pointer;}#chatgpt-mermaid-\_r_1aj\_ .root .anchor path{fill:rgb(143, 143, 143)!important;stroke-width:0;stroke:rgb(143, 143, 143);}#chatgpt-mermaid-\_r_1aj\_ .arrowheadPath{fill:rgb(143, 143, 143);}#chatgpt-mermaid-\_r_1aj\_ .edgePath .path{stroke:rgb(143, 143, 143);stroke-width:1px;}#chatgpt-mermaid-\_r_1aj\_ .flowchart-link{stroke:rgb(143, 143, 143);fill:none;}#chatgpt-mermaid-\_r_1aj\_ .edgeLabel{background-color:rgb(252, 252, 252);text-align:center;}#chatgpt-mermaid-\_r_1aj\_ .edgeLabel p{background-color:rgb(252, 252, 252);}#chatgpt-mermaid-\_r_1aj\_ .edgeLabel rect{opacity:0.5;background-color:rgb(252, 252, 252);fill:rgb(252, 252, 252);}#chatgpt-mermaid-\_r_1aj\_ .labelBkg{background-color:rgba(252, 252, 252, 0.5);}#chatgpt-mermaid-\_r_1aj\_ .cluster rect{fill:rgb(243, 243, 243);stroke:rgba(0, 0, 0, 0.1);stroke-width:1px;}#chatgpt-mermaid-\_r_1aj\_ .cluster text{fill:rgb(13, 13, 13);}#chatgpt-mermaid-\_r_1aj\_ .cluster span{color:rgb(13, 13, 13);}#chatgpt-mermaid-\_r_1aj\_ div.mermaidTooltip{position:absolute;text-align:center;max-width:200px;padding:2px;font-family:-apple-system-body,ui-sans-serif,-apple-system,system-ui,"Segoe UI",Helvetica,"Apple Color Emoji",Arial,sans-serif,"Segoe UI Emoji","Segoe UI Symbol";font-size:12px;background:rgb(243, 243, 243);border:1px solid rgba(0, 0, 0, 0.1);border-radius:2px;pointer-events:none;z-index:100;}#chatgpt-mermaid-\_r_1aj\_ .flowchartTitleText{text-anchor:middle;font-size:18px;fill:rgb(13, 13, 13);}#chatgpt-mermaid-\_r_1aj\_ rect.text{fill:none;stroke-width:0;}#chatgpt-mermaid-\_r_1aj\_ .icon-shape,#chatgpt-mermaid-\_r_1aj\_ .image-shape{background-color:rgb(252, 252, 252);text-align:center;}#chatgpt-mermaid-\_r_1aj\_ .icon-shape p,#chatgpt-mermaid-\_r_1aj\_ .image-shape p{background-color:rgb(252, 252, 252);padding:2px;}#chatgpt-mermaid-\_r_1aj\_ .icon-shape .label rect,#chatgpt-mermaid-\_r_1aj\_ .image-shape .label rect{opacity:0.5;background-color:rgb(252, 252, 252);fill:rgb(252, 252, 252);}#chatgpt-mermaid-\_r_1aj\_ .label-icon{display:inline-block;height:1em;overflow:visible;vertical-align:-0.125em;}#chatgpt-mermaid-\_r_1aj\_ .node .label-icon path{fill:currentColor;stroke:revert;stroke-width:revert;}#chatgpt-mermaid-\_r_1aj\_ .node .neo-node{stroke:rgb(83, 154, 248);}#chatgpt-mermaid-\_r_1aj\_ [data-look="neo"].node rect,#chatgpt-mermaid-\_r_1aj\_ [data-look="neo"].cluster rect,#chatgpt-mermaid-\_r_1aj\_ [data-look="neo"].node polygon{stroke:url(#chatgpt-mermaid-\_r_1aj\_-gradient);filter:drop-shadow( 1px 2px 2px rgba(185,185,185,1));}#chatgpt-mermaid-\_r_1aj\_ [data-look="neo"].swimlane.cluster rect{filter:none;}#chatgpt-mermaid-\_r_1aj\_ [data-look="neo"].node path{stroke:url(#chatgpt-mermaid-\_r_1aj\_-gradient);stroke-width:1px;}#chatgpt-mermaid-\_r_1aj\_ [data-look="neo"].node .outer-path{filter:drop-shadow( 1px 2px 2px rgba(185,185,185,1));}#chatgpt-mermaid-\_r_1aj\_ [data-look="neo"].node .neo-line path{stroke:rgb(83, 154, 248);filter:none;}#chatgpt-mermaid-\_r_1aj\_ [data-look="neo"].node circle{stroke:url(#chatgpt-mermaid-\_r_1aj\_-gradient);filter:drop-shadow( 1px 2px 2px rgba(185,185,185,1));}#chatgpt-mermaid-\_r_1aj\_ [data-look="neo"].node circle .state-start{fill:#000000;}#chatgpt-mermaid-\_r_1aj\_ [data-look="neo"].icon-shape .icon{fill:url(#chatgpt-mermaid-\_r_1aj\_-gradient);filter:drop-shadow( 1px 2px 2px rgba(185,185,185,1));}#chatgpt-mermaid-\_r_1aj\_ [data-look="neo"].icon-shape .icon-neo path{stroke:url(#chatgpt-mermaid-\_r_1aj\_-gradient);filter:drop-shadow( 1px 2px 2px rgba(185,185,185,1));}#chatgpt-mermaid-\_r_1aj\_ .node text{font-size:14px;font-weight:600;letter-spacing:normal;fill:rgb(0, 79, 153);}#chatgpt-mermaid-\_r_1aj\_ .edgeLabels text{font-size:13px;font-weight:600;letter-spacing:-0.08px;fill:rgb(0, 79, 153);}#chatgpt-mermaid-\_r_1aj\_ .node tspan[font-weight="normal"],#chatgpt-mermaid-\_r_1aj\_ .edgeLabels tspan[font-weight="normal"]{font-weight:600;}#chatgpt-mermaid-\_r_1aj\_ .edgeLabel .label rect{opacity:1;rx:13px;ry:13px;fill:rgb(245, 250, 255);stroke:rgb(206, 219, 229);stroke-width:1px;}#chatgpt-mermaid-\_r_1aj\_ .node rect,#chatgpt-mermaid-\_r_1aj\_ .node circle,#chatgpt-mermaid-\_r_1aj\_ .node ellipse,#chatgpt-mermaid-\_r_1aj\_ .node polygon,#chatgpt-mermaid-\_r_1aj\_ .node path{fill:rgb(229, 243, 255);stroke:rgba(0, 0, 0, 0.1);stroke-width:1px;}#chatgpt-mermaid-\_r_1aj\_ .node rect{rx:16px;ry:16px;}#chatgpt-mermaid-\_r_1aj\_ .mermaid-decision .label-container{fill:rgb(245, 250, 255);stroke:rgb(206, 219, 229);stroke-dasharray:2,2;}#chatgpt-mermaid-\_r_1aj\_ .edgePaths .flowchart-link{stroke:rgb(143, 143, 143);stroke-width:1px;stroke-linecap:round;stroke-linejoin:round;}#chatgpt-mermaid-\_r_1aj\_ .marker{fill:rgb(143, 143, 143);stroke:rgb(143, 143, 143);}#chatgpt-mermaid-\_r_1aj\_ :root{--mermaid-font-family:-apple-system-body,ui-sans-serif,-apple-system,system-ui,"Segoe UI",Helvetica,"Apple Color Emoji",Arial,sans-serif,"Segoe UI Emoji","Segoe UI Symbol";}CLI entry pointParse and validate argumentsParse GitHub URLResolve ref and folderPrimary GitHub APIdownloaderPrimary retrieval succeeds?Stage and validate filesArchive fallbackDownload and validate archiveSafe selective extractionCommit to destinationReport resultsYesNo

### **Proposed functions**

| Function                        | Responsibility                          |
| ------------------------------- | --------------------------------------- |
| `main()`                        | CLI orchestration                       |
| `parse_args()`                  | Argument parsing                        |
| `parse_github_folder_url()`     | Parse and validate GitHub URL           |
| `resolve_github_ref()`          | Resolve branch, tag or commit ref       |
| `resolve_target_directory()`    | Confirm target directory                |
| `fetch_tree()`                  | Retrieve GitHub tree metadata           |
| `download_file()`               | Download individual file safely         |
| `download_folder_api()`         | Reconstruct target folder               |
| `download_repository_archive()` | Download ZIP or TAR.GZ                  |
| `validate_archive()`            | Validate archive format and constraints |
| `extract_target_from_archive()` | Safely extract target folder            |
| `validate_staged_content()`     | Validate reconstructed files            |
| `commit_staged_content()`       | Copy/move staged files to destination   |
| `preserve_failed_archive()`     | Save archive if extraction fails        |
| `report_results()`              | Report files, size, method and errors   |

## **11. Failure-handling matrix**

| Failure                       | Recommended response                                                      |
| ----------------------------- | ------------------------------------------------------------------------- |
| Invalid GitHub URL            | Abort; explain expected URL format.                                       |
| Unsupported host              | Abort; explain that GitHub URLs are supported.                            |
| Repository not found          | Report repository or permission error.                                    |
| Branch/ref cannot be resolved | Report ambiguity or unresolved ref.                                       |
| Target folder not found       | Abort or attempt a carefully defined fallback resolution.                 |
| API rate limit                | Report rate limit; optionally retry if appropriate.                       |
| Direct file download fails    | Attempt alternative API/tree retrieval if feasible.                       |
| Primary retrieval fails       | Attempt repository archive fallback.                                      |
| ZIP download fails            | Attempt TAR.GZ fallback.                                                  |
| TAR.GZ download fails         | Report failure.                                                           |
| Archive invalid               | Preserve archive if downloaded; report validation failure.                |
| Extraction fails              | Preserve archive in destination; report extraction failure.               |
| Unsafe archive entry          | Reject entry; never extract it.                                           |
| Disk write fails              | Clean up staging; report error.                                           |
| Destination conflict          | Follow overwrite policy.                                                  |
| Both methods fail             | Return a nonzero exit code.                                               |
| Interrupted execution         | Clean temporary staging when possible; retain previously committed files. |

## **12. Testing and validation plan**

The implementation should be tested against a structured test matrix rather than merely tested against one public repository.

### **A. URL parsing tests**

- Standard branch URL.
- Branch name containing slashes.
- URL-encoded folder names.
- Repository root.
- Folder path with nested directories.
- Tag URL.
- Commit URL.
- Invalid URL.
- Unsupported URL format.
- Ambiguous ref/path.
- Malformed URL.

### **B. Download tests**

- Public repository.
- Small folder.
- Large folder.
- Folder containing nested directories.
- Folder containing binary files.
- Folder containing Markdown.
- Folder containing unusual filenames.
- Folder containing non-ASCII names.
- API rate-limit response.
- HTTP 404.
- HTTP 403.
- HTTP 429.
- HTTP 500.
- Timeout.
- Connection interruption.

### **C. Archive tests**

- Valid ZIP.
- Valid TAR.GZ.
- Corrupted ZIP.
- Corrupted TAR.GZ.
- Empty archive.
- Archive with unexpected root structure.
- Archive with path traversal entries.
- Archive with absolute paths.
- Archive with symlinks.
- Archive with hard links.
- Archive with special files.
- Archive with excessive file count.
- Archive exceeding download limits.
- Archive exceeding extraction limits.
- Archive containing the requested directory.
- Archive missing the requested directory.

### **D. Destination tests**

- Destination does not exist.
- Destination exists and is empty.
- Destination exists with unrelated files.
- Existing conflicting files.
- No-overwrite mode.
- Read-only destination.
- Invalid destination path.
- Insufficient disk space.
- Interrupted commit.

### **E. Integrity and correctness tests**

For successful retrieval:

- Verify that all expected files exist.
- Verify directory structure.
- Verify file contents.
- Compare hashes of downloaded files against the retrieved source metadata when available.
- Verify that no unexpected files were written.
- Verify that files were not executed.
- Verify that the archive was removed or retained according to policy.
- Verify that the exit code is correct.

**Testing should use mock HTTP responses for most cases.** This avoids depending on GitHub availability, rate limits, or mutable repository contents for routine regression tests.

## **13. Definition of Done**

**The improved script will be considered complete when:**

- It accepts exactly two required positional inputs for the basic invocation.
- It parses supported GitHub folder URLs correctly.
- It can resolve branches containing slashes, where resolution is unambiguous.
- It downloads only the requested folder using its primary retrieval mechanism.
- It preserves the requested folder's internal layout.
- It avoids unnecessarily downloading the entire repository.
- It uses a repository archive as a fallback.
- It supports ZIP and TAR.GZ fallback paths.
- It safely extracts only the requested folder.
- It preserves the original archive when extraction fails.
- It protects against path traversal and unsafe archive entries.
- It imposes configurable resource limits.
- It handles existing destination files predictably.
- It uses staging and controlled commits.
- It provides useful diagnostic output.
- It returns meaningful exit codes.
- It never executes downloaded content.
- It has automated tests for core functionality and failure scenarios.

## **14. Final implementation recommendation**

**I recommend implementing this as a single-file Python 3.11+ utility with a modular internal design, using the standard library and GitHub's API for the primary retrieval method.**

The implementation priority should be:

1. Correct URL parsing and ref resolution.
2. Reliable targeted folder retrieval.
3. Faithful directory reconstruction.
4. Safe ZIP/TAR.GZ fallback.
5. Archive preservation upon extraction failure.
6. Transactional destination handling.
7. Resource limits and security validation.
8. Meaningful CLI diagnostics and exit codes.
9. Automated tests and evidence-based verification.

This architecture would make the utility useful for retrieving standalone GitHub skills, agent instructions, templates, documentation directories, example projects and other repository subfolders without requiring the user to clone an entire repository.

## **15. Implementation delivered**

**The standalone Python script has been created and passed Python compilation.**

I also performed smoke tests covering:

- GitHub folder URL parsing.
- GitHub repository root URL parsing.
- Rejection of traversal-style paths.
- Archive-root and target-folder path calculation.
- Archive URL generation.

**The smoke tests passed.**

**I have not performed live GitHub download tests.** The script's real network behavior, rate-limit handling against live GitHub, and actual ZIP/TAR.GZ extraction against live repository archives remain unverified.

### **Download the script**

**github_folder_downloader.py**

Standalone Python CLI utility

Python compilation verified

Download the Python script

### **16. Usage guide**

#### **Basic usage**

```
python github_folder_downloader.py \
  "https://github.com/nordeim/my-pi-agent/tree/main/skills/solving-a-level-exam-papers" \
  "/tmp/skill"
```

This will:

1. Resolve the GitHub repository and target folder.
2. Retrieve the folder's contents using GitHub API/raw-file retrieval.
3. Reconstruct the directory structure inside `/tmp/skill`.
4. If the primary retrieval fails, attempt ZIP and TAR.GZ repository archive fallbacks.
5. Preserve a downloaded archive if its extraction or processing fails.
6. Report the outcome.

#### **Windows example**

```
python github_folder_downloader.py `
  "https://github.com/OWNER/REPO/tree/main/path/to/folder" `
  "C:\Downloads\GitHubFolder"
```

#### **Linux example**

```
python3 github_folder_downloader.py \
  "https://github.com/OWNER/REPO/tree/main/path/to/folder" \
  "$HOME/Downloads/GitHubFolder"
```

#### **Verbose diagnostics**

```
python github_folder_downloader.py \
  "https://github.com/OWNER/REPO/tree/main/path/to/folder" \
  "/tmp/download" \
  --verbose
```

#### **Preserve the archive even after successful extraction**

```
python github_folder_downloader.py \
  "https://github.com/OWNER/REPO/tree/main/path/to/folder" \
  "/tmp/download" \
  --keep-archive
```

#### **Refuse to overwrite existing files**

```
python github_folder_downloader.py \
  "https://github.com/OWNER/REPO/tree/main/path/to/folder" \
  "/tmp/download" \
  --no-overwrite
```

#### **Optional GitHub authentication**

On Linux:

```
export GITHUB_TOKEN="your-token"
```

On PowerShell:

```
$env:GITHUB_TOKEN = "your-token"
```

Then run the script normally. The token is read from the environment variable and is not embedded in the script.

**Use a token with the minimum required permissions, and avoid sharing terminal logs that might expose credentials.**

**My recommendation:** Before relying on this script for automated AI-agent skill installation or retrieval, the next validation stage should be a dedicated automated test suite covering mocked GitHub API responses, branch names containing slashes, ZIP/TAR.GZ extraction, path traversal, interrupted downloads, file conflicts and rollback behavior.

That would bring it closer to a genuinely production-ready downloader rather than simply a compiled and smoke-tested utility.

---

## File: `github_folder_downloader.py`
```python
#!/usr/bin/env python3
"""Download and mirror a GitHub repository folder without cloning the whole repository.

Usage:
  python github_folder_downloader.py URL DESTINATION
  python github_folder_downloader.py URL DESTINATION --verbose

Only ordinary files and directories are materialized. Archive fallback is never
executed. See --help for limits and options.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import logging
import os
import re
import shutil
import stat
import sys
import tempfile
import time
import urllib.error
import urllib.parse
import urllib.request
import zipfile
import tarfile
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from typing import Iterable

LOG = logging.getLogger("github-folder-downloader")
USER_AGENT = "github-folder-downloader/1.0 (Python urllib)"
API_BASE = "https://api.github.com"
RAW_BASE = "https://raw.githubusercontent.com"
DEFAULT_MAX_DOWNLOAD = 100 * 1024 * 1024
DEFAULT_MAX_EXTRACT = 250 * 1024 * 1024
DEFAULT_MAX_FILES = 5000
DEFAULT_MAX_DEPTH = 100
CHUNK = 64 * 1024


class DownloadError(Exception):
    """Expected operational failure."""


@dataclass(frozen=True)
class RepoTarget:
    owner: str
    repo: str
    ref: str
    path: str
    commit_sha: str
    tree_sha: str


def safe_relpath(path: str) -> PurePosixPath:
    """Validate an archive or repository path as relative and traversal-free."""
    path = path.replace("\\", "/")
    p = PurePosixPath(path)
    if p.is_absolute() or not path or any(part in ("", ".", "..") for part in p.parts):
        raise DownloadError(f"Unsafe or invalid relative path: {path!r}")
    if any(":" in part for part in p.parts):
        # Conservative protection against drive-like paths and odd path syntax.
        raise DownloadError(f"Unsafe path component: {path!r}")
    return p


def request_bytes(url: str, *, timeout: float, token: str | None = None,
                  accept: str = "application/vnd.github+json",
                  limit: int | None = None) -> bytes:
    if not url.lower().startswith("https://"):
        raise DownloadError("HTTPS is required for network requests.")
    headers = {"User-Agent": USER_AGENT, "Accept": accept}
    if token:
        headers["Authorization"] = "Bearer " + token
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as response:
            content_length = response.headers.get("Content-Length")
            if limit is not None and content_length:
                try:
                    if int(content_length) > limit:
                        raise DownloadError(f"Response exceeds size limit ({limit} bytes).")
                except ValueError:
                    pass
            chunks, total = [], 0
            while True:
                chunk = response.read(CHUNK)
                if not chunk:
                    break
                total += len(chunk)
                if limit is not None and total > limit:
                    raise DownloadError(f"Response exceeds size limit ({limit} bytes).")
                chunks.append(chunk)
            return b"".join(chunks)
    except urllib.error.HTTPError as exc:
        detail = exc.read(1024).decode("utf-8", "replace")
        raise DownloadError(f"HTTP {exc.code} for {url}: {detail[:300]}") from exc
    except urllib.error.URLError as exc:
        raise DownloadError(f"Network error for {url}: {exc.reason}") from exc
    except TimeoutError as exc:
        raise DownloadError(f"Timed out requesting {url}") from exc


def api_json(url: str, *, timeout: float, token: str | None):
    payload = request_bytes(url, timeout=timeout, token=token, limit=10 * 1024 * 1024)
    try:
        return json.loads(payload.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise DownloadError(f"Invalid JSON response from GitHub API: {url}") from exc


def encode_path(path: str) -> str:
    return "/".join(urllib.parse.quote(part, safe="") for part in path.split("/") if part)


def parse_url(url: str) -> tuple[str, str, list[str], str]:
    """Parse github.com owner/repo tree URL, returning owner, repo, tail, kind."""
    try:
        parsed = urllib.parse.urlsplit(url)
    except ValueError as exc:
        raise DownloadError(f"Invalid URL: {exc}") from exc
    if parsed.scheme != "https" or parsed.hostname != "github.com" or parsed.username or parsed.password:
        raise DownloadError("Expected an HTTPS github.com URL.")
    if parsed.query or parsed.fragment:
        raise DownloadError("Query strings and fragments are not supported in folder URLs.")
    parts = [urllib.parse.unquote(p) for p in parsed.path.strip("/").split("/") if p]
    if len(parts) < 2:
        raise DownloadError("URL must include OWNER and REPO.")
    owner, repo = parts[0], parts[1]
    if repo.endswith(".git"):
        repo = repo[:-4]
    if not owner or not repo or any("/" in x or x in (".", "..") for x in (owner, repo)):
        raise DownloadError("Invalid owner or repository name.")
    if len(parts) == 2:
        return owner, repo, [], "root"
    if parts[2] != "tree" or len(parts) < 4:
        raise DownloadError("Expected a folder URL in the form https://github.com/OWNER/REPO/tree/REF/PATH.")
    return owner, repo, parts[3:], "tree"


def get_repo_default_branch(owner: str, repo: str, *, timeout: float, token: str | None) -> str:
    data = api_json(f"{API_BASE}/repos/{encode_path(owner)}/{encode_path(repo)}",
                    timeout=timeout, token=token)
    branch = data.get("default_branch")
    if not isinstance(branch, str) or not branch:
        raise DownloadError("Could not determine repository default branch.")
    return branch


def resolve_target(owner: str, repo: str, tail: list[str], kind: str, *,
                  timeout: float, token: str | None) -> RepoTarget:
    if kind == "root":
        ref = get_repo_default_branch(owner, repo, timeout=timeout, token=token)
        path = ""
        commit_data = api_json(f"{API_BASE}/repos/{encode_path(owner)}/{encode_path(repo)}/commits/{encode_path(ref)}",
                              timeout=timeout, token=token)
        commit = commit_data.get("sha")
        tree_sha = (commit_data.get("commit") or {}).get("tree", {}).get("sha")
        if not commit or not tree_sha:
            raise DownloadError("Could not resolve default branch commit and tree.")
        return RepoTarget(owner, repo, ref, path, commit, tree_sha)

    # Resolve ref/path ambiguity by trying the longest possible ref prefix first.
    for split in range(len(tail), 0, -1):
        candidate_ref = "/".join(tail[:split])
        candidate_path = "/".join(tail[split:])
        if not candidate_ref:
            continue
        try:
            commit_data = api_json(
                f"{API_BASE}/repos/{encode_path(owner)}/{encode_path(repo)}/commits/{encode_path(candidate_ref)}",
                timeout=timeout, token=token)
            sha = commit_data.get("sha")
            tree_sha = (commit_data.get("commit") or {}).get("tree", {}).get("sha")
            if not sha or not tree_sha:
                continue
            target_path = candidate_path.strip("/")
            # Confirm directory existence using tree listing at the resolved commit.
            tree = fetch_tree(tree_sha, "", owner, repo, timeout=timeout, token=token)
            if target_path:
                found = any(item["path"] == target_path and item["type"] == "tree" for item in tree)
                # Tree response here is the root tree; nested directory paths are not in
                # a non-recursive tree. Use recursive tree endpoint to verify the path.
                recursive = api_json(
                    f"{API_BASE}/repos/{encode_path(owner)}/{encode_path(repo)}/git/trees/{encode_path(tree_sha)}?recursive=1",
                    timeout=timeout, token=token)
                if recursive.get("truncated"):
                    # Exact path may still be found in returned entries, but truncation
                    # makes this resolution less reliable; try another candidate.
                    continue
                found = any(x.get("path") == target_path and x.get("type") == "tree"
                            for x in recursive.get("tree", []))
                if not found:
                    continue
            return RepoTarget(owner, repo, candidate_ref, target_path, sha, tree_sha)
        except DownloadError:
            continue
    raise DownloadError("Could not resolve URL ref and folder path. Check the URL; branch names with slashes may be ambiguous.")


def fetch_tree(tree_sha: str, prefix: str, owner: str, repo: str, *,
               timeout: float, token: str | None) -> list[dict]:
    """Fetch non-recursive trees, recursively walking folders, without tree truncation."""
    data = api_json(f"{API_BASE}/repos/{encode_path(owner)}/{encode_path(repo)}/git/trees/{encode_path(tree_sha)}",
                    timeout=timeout, token=token)
    if not isinstance(data.get("tree"), list):
        raise DownloadError("Unexpected GitHub tree response.")
    entries = []
    for item in data["tree"]:
        name = item.get("path")
        typ = item.get("type")
        sha = item.get("sha")
        if not isinstance(name, str) or typ not in ("blob", "tree") or not sha:
            continue
        rel = f"{prefix}/{name}" if prefix else name
        if typ == "blob":
            entries.append({"path": rel, "type": "blob", "sha": sha, "size": item.get("size", 0)})
        else:
            entries.append({"path": rel, "type": "tree", "sha": sha, "size": 0})
            entries.extend(fetch_tree(sha, rel, owner, repo, timeout=timeout, token=token))
    return entries


def download_blob(target: RepoTarget, path: str, *, timeout: float, token: str | None,
                  max_size: int) -> bytes:
    url = f"{RAW_BASE}/{encode_path(target.owner)}/{encode_path(target.repo)}/{encode_path(target.ref)}/{encode_path(path)}"
    return request_bytes(url, timeout=timeout, token=token, accept="application/octet-stream", limit=max_size)


def stage_api_folder(target: RepoTarget, stage: Path, *, timeout: float, token: str | None,
                     max_download: int, max_files: int, max_depth: int) -> tuple[int, int]:
    entries = fetch_tree(target.tree_sha, "", target.owner, target.repo, timeout=timeout, token=token)
    prefix = target.path.strip("/")
    selected = []
    for entry in entries:
        if entry["type"] != "blob":
            continue
        p = entry["path"]
        if prefix:
            if not p.startswith(prefix + "/"):
                continue
            rel = p[len(prefix) + 1:]
        else:
            rel = p
        if not rel:
            continue
        safe = safe_relpath(rel)
        if len(safe.parts) > max_depth:
            raise DownloadError(f"Folder depth exceeds configured limit ({max_depth}).")
        selected.append((entry, rel))
    if len(selected) > max_files:
        raise DownloadError(f"Folder contains more than {max_files} files.")
    total = 0
    for entry, rel in selected:
        size = entry.get("size")
        if isinstance(size, int) and size > max_download:
            raise DownloadError(f"File exceeds per-download limit: {rel}")
        data = download_blob(target, entry["path"], timeout=timeout, token=token, max_size=max_download)
        total += len(data)
        if total > max_download:
            raise DownloadError(f"Folder download exceeds aggregate download limit ({max_download} bytes).")
        dest = stage.joinpath(*safe_relpath(rel).parts)
        dest.parent.mkdir(parents=True, exist_ok=True)
        with dest.open("wb") as fh:
            fh.write(data)
    return len(selected), total


def stream_to_file(url: str, out: Path, *, timeout: float, token: str | None,
                   max_size: int, accept: str = "application/octet-stream") -> int:
    if not url.startswith("https://"):
        raise DownloadError("HTTPS is required for archive downloads.")
    headers = {"User-Agent": USER_AGENT, "Accept": accept}
    if token:
        headers["Authorization"] = "Bearer " + token
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as response, out.open("wb") as fh:
            length = response.headers.get("Content-Length")
            if length:
                try:
                    if int(length) > max_size:
                        raise DownloadError("Archive exceeds configured download limit.")
                except ValueError:
                    pass
            total = 0
            while True:
                chunk = response.read(CHUNK)
                if not chunk:
                    break
                total += len(chunk)
                if total > max_size:
                    raise DownloadError("Archive exceeds configured download limit.")
                fh.write(chunk)
            return total
    except urllib.error.HTTPError as exc:
        detail = exc.read(1024).decode("utf-8", "replace")
        raise DownloadError(f"HTTP {exc.code} downloading archive: {detail[:300]}") from exc
    except urllib.error.URLError as exc:
        raise DownloadError(f"Archive network error: {exc.reason}") from exc
    except TimeoutError as exc:
        raise DownloadError("Archive download timed out.") from exc


def archive_urls(target: RepoTarget) -> list[tuple[str, str]]:
    # Use the resolved commit SHA so archive retrieval is reproducible and avoids
    # ambiguity between branch names, tags, and refs containing slashes.
    commit = urllib.parse.quote(target.commit_sha, safe="")
    return [
        ("zip", f"https://codeload.github.com/{target.owner}/{target.repo}/zip/{commit}"),
        ("tar.gz", f"https://codeload.github.com/{target.owner}/{target.repo}/tar.gz/{commit}"),
    ]


def archive_prefix(target: RepoTarget, members: Iterable[str]) -> str:
    # GitHub archives have one top-level directory; determine its name and ensure
    # the target path occurs below that root.
    roots = set()
    for name in members:
        parts = [p for p in name.replace("\\", "/").split("/") if p]
        if parts:
            roots.add(parts[0])
    if len(roots) != 1:
        raise DownloadError("Archive has an unexpected root structure.")
    root = next(iter(roots))
    return root + ("/" + target.path.strip("/") if target.path.strip("/") else "")


def extract_zip_target(archive: Path, stage: Path, target: RepoTarget, *,
                       max_extract: int, max_files: int, max_depth: int) -> tuple[int, int]:
    with zipfile.ZipFile(archive) as zf:
        names = [i.filename for i in zf.infolist()]
        prefix = archive_prefix(target, names).rstrip("/") + "/"
        selected = []
        total = 0
        for info in zf.infolist():
            name = info.filename.replace("\\", "/")
            if not name.startswith(prefix) or name.endswith("/"):
                continue
            rel = name[len(prefix):]
            if not rel:
                continue
            p = safe_relpath(rel)
            if len(p.parts) > max_depth:
                raise DownloadError("Archive folder depth exceeds limit.")
            if info.is_dir():
                continue
            # Reject symlinks and non-regular entries via Unix mode metadata.
            mode = (info.external_attr >> 16) & 0xFFFF
            if mode and stat.S_IFMT(mode) not in (0, stat.S_IFREG):
                raise DownloadError(f"ZIP contains a non-regular entry: {rel}")
            if info.file_size < 0 or info.file_size > max_extract:
                raise DownloadError(f"ZIP entry exceeds extraction limit: {rel}")
            total += info.file_size
            if total > max_extract:
                raise DownloadError("ZIP extracted content exceeds size limit.")
            selected.append((info, rel))
        if len(selected) > max_files:
            raise DownloadError("ZIP extracted file count exceeds limit.")
        for info, rel in selected:
            p = safe_relpath(rel)
            dest = stage.joinpath(*p.parts)
            dest.parent.mkdir(parents=True, exist_ok=True)
            with zf.open(info) as src, dest.open("wb") as dst:
                shutil.copyfileobj(src, dst, CHUNK)
        return len(selected), total


def extract_tar_target(archive: Path, stage: Path, target: RepoTarget, *,
                       max_extract: int, max_files: int, max_depth: int) -> tuple[int, int]:
    with tarfile.open(archive, "r:gz") as tf:
        names = [m.name for m in tf.getmembers()]
        prefix = archive_prefix(target, names).rstrip("/") + "/"
        selected = []
        total = 0
        for member in tf.getmembers():
            name = member.name.replace("\\", "/")
            if not name.startswith(prefix) or member.isdir():
                continue
            rel = name[len(prefix):]
            if not rel:
                continue
            p = safe_relpath(rel)
            if len(p.parts) > max_depth:
                raise DownloadError("TAR extracted folder depth exceeds limit.")
            if not member.isfile():
                raise DownloadError(f"TAR contains a non-regular entry: {rel}")
            if member.size < 0 or member.size > max_extract:
                raise DownloadError(f"TAR entry exceeds extraction limit: {rel}")
            total += member.size
            if total > max_extract:
                raise DownloadError("TAR extracted content exceeds size limit.")
            selected.append((member, rel))
        if len(selected) > max_files:
            raise DownloadError("TAR extracted file count exceeds limit.")
        for member, rel in selected:
            p = safe_relpath(rel)
            dest = stage.joinpath(*p.parts)
            dest.parent.mkdir(parents=True, exist_ok=True)
            src = tf.extractfile(member)
            if src is None:
                raise DownloadError(f"Unable to read archive member: {rel}")
            with src, dest.open("wb") as dst:
                shutil.copyfileobj(src, dst, CHUNK)
        return len(selected), total


def commit_files(stage: Path, destination: Path, *, no_overwrite: bool) -> int:
    """Controlled per-file commit with rollback of overwritten files on failure."""
    files = [p for p in stage.rglob("*") if p.is_file()]
    backup = stage / ".rollback"
    backup.mkdir(exist_ok=True)
    installed, backed_up = [], []
    try:
        for src in files:
            rel = src.relative_to(stage)
            dst = destination / rel
            if dst.exists():
                if dst.is_dir():
                    raise DownloadError(f"Destination conflict: {dst} is a directory.")
                if no_overwrite:
                    raise DownloadError(f"File exists and --no-overwrite is set: {dst}")
                backup_path = backup / rel
                backup_path.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(dst, backup_path)
                backed_up.append((dst, backup_path))
            dst.parent.mkdir(parents=True, exist_ok=True)
            tmp = dst.with_name(dst.name + ".tmp-download")
            shutil.copyfile(src, tmp)
            os.replace(tmp, dst)
            installed.append(dst)
    except Exception:
        for dst in reversed(installed):
            try:
                dst.unlink(missing_ok=True)
            except OSError:
                pass
        for dst, backup_path in reversed(backed_up):
            try:
                dst.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(backup_path, dst)
            except OSError:
                LOG.exception("Rollback failed for %s", dst)
        raise
    return len(files)


def preserve_archive(archive: Path, destination: Path, name: str) -> Path:
    destination.mkdir(parents=True, exist_ok=True)
    safe_name = re.sub(r"[^A-Za-z0-9._-]+", "-", name).strip("-") or "repository"
    dest = destination / f"{safe_name}-fallback{archive.suffix if archive.suffix else '.archive'}"
    # TAR.GZ suffix handling: Path.suffix yields '.gz'; keep recognizable extension.
    if archive.name.endswith(".tar.gz"):
        dest = destination / f"{safe_name}-fallback.tar.gz"
    shutil.copyfile(archive, dest)
    return dest


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(CHUNK), b""):
            h.update(chunk)
    return h.hexdigest()


def download_with_archive_fallback(target: RepoTarget, destination: Path, *, timeout: float,
                                  token: str | None, max_download: int,
                                  max_extract: int, max_files: int, max_depth: int,
                                  keep_archive: bool, no_overwrite: bool) -> tuple[int, int, str]:
    errors = []
    destination.mkdir(parents=True, exist_ok=True)
    for fmt, url in archive_urls(target):
        with tempfile.TemporaryDirectory(prefix="gh-folder-") as tmp:
            tmpdir = Path(tmp)
            archive = tmpdir / ("repo.zip" if fmt == "zip" else "repo.tar.gz")
            try:
                archive_bytes = stream_to_file(url, archive, timeout=timeout, token=token,
                                              max_size=max_download)
                stage = tmpdir / "stage"
                stage.mkdir()
                if fmt == "zip":
                    result = extract_zip_target(archive, stage, target, max_extract=max_extract,
                                               max_files=max_files, max_depth=max_depth)
                else:
                    result = extract_tar_target(archive, stage, target, max_extract=max_extract,
                                               max_files=max_files, max_depth=max_depth)
                commit_files(stage, destination, no_overwrite=no_overwrite)
                if keep_archive:
                    saved = destination / ("repository-fallback.zip" if fmt == "zip" else "repository-fallback.tar.gz")
                    shutil.copyfile(archive, saved)
                    LOG.info("Retained archive: %s", saved)
                return result[0], result[1], fmt
            except Exception as exc:
                errors.append(f"{fmt}: {exc}")
                LOG.warning("%s fallback failed: %s", fmt.upper(), exc)
                # Preserve a successfully downloaded archive if extraction or commit
                # failed; if download failed, there is nothing to retain.
                if archive.exists() and archive.stat().st_size:
                    try:
                        saved = preserve_archive(archive, destination, f"{target.repo}-{target.ref}")
                        LOG.warning("Preserved archive for manual recovery: %s", saved)
                    except OSError as save_exc:
                        errors.append(f"preservation failed: {save_exc}")
    raise DownloadError("Archive fallback failed: " + " | ".join(errors))


def parse_args(argv=None):
    parser = argparse.ArgumentParser(
        description="Download and mirror a GitHub repository folder without cloning the entire repository.")
    parser.add_argument("github_folder_url", help="HTTPS GitHub repository folder URL, or repository root URL")
    parser.add_argument("destination", help="Local destination directory")
    parser.add_argument("--timeout", type=float, default=30.0, help="Network operation timeout in seconds (default: 30)")
    parser.add_argument("--max-download-size", type=int, default=100,
                       help="Maximum download size in MiB (default: 100)")
    parser.add_argument("--max-extracted-size", type=int, default=250,
                       help="Maximum extracted folder size in MiB (default: 250)")
    parser.add_argument("--max-files", type=int, default=DEFAULT_MAX_FILES,
                       help=f"Maximum files to materialize (default: {DEFAULT_MAX_FILES})")
    parser.add_argument("--max-depth", type=int, default=DEFAULT_MAX_DEPTH,
                       help=f"Maximum path depth (default: {DEFAULT_MAX_DEPTH})")
    parser.add_argument("--keep-archive", action="store_true", help="Retain archive even after successful extraction")
    parser.add_argument("--no-overwrite", action="store_true", help="Refuse to overwrite existing destination files")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose logging")
    parser.add_argument("--token-env", default="GITHUB_TOKEN", help="Environment variable containing GitHub token (default: GITHUB_TOKEN)")
    args = parser.parse_args(argv)
    if args.timeout <= 0 or args.max_download_size <= 0 or args.max_extracted_size <= 0 or args.max_files <= 0 or args.max_depth <= 0:
        parser.error("Timeout and all size/count/depth limits must be positive.")
    return args


def main(argv=None) -> int:
    args = parse_args(argv)
    logging.basicConfig(level=logging.DEBUG if args.verbose else logging.INFO,
                        format="%(levelname)s: %(message)s")
    destination = Path(args.destination).expanduser().resolve()
    if destination.exists() and not destination.is_dir():
        LOG.error("Destination exists but is not a directory: %s", destination)
        return 2
    token = os.environ.get(args.token_env) or None
    max_download = args.max_download_size * 1024 * 1024
    max_extract = args.max_extracted_size * 1024 * 1024
    try:
        owner, repo, tail, kind = parse_url(args.github_folder_url)
        target = resolve_target(owner, repo, tail, kind, timeout=args.timeout, token=token)
        LOG.info("Resolved repository=%s/%s ref=%s path=%s",
                 target.owner, target.repo, target.ref, target.path or "(repository root)")
        destination.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory(prefix="gh-folder-primary-") as tmp:
            stage = Path(tmp) / "stage"
            stage.mkdir()
            try:
                count, size = stage_api_folder(target, stage, timeout=args.timeout, token=token,
                                               max_download=max_download, max_files=args.max_files,
                                               max_depth=args.max_depth)
                commit_files(stage, destination, no_overwrite=args.no_overwrite)
                LOG.info("SUCCESS: downloaded %d file(s), %.2f MiB using GitHub API/raw retrieval.",
                         count, size / (1024 * 1024))
                return 0
            except Exception as primary_exc:
                LOG.warning("Primary retrieval failed: %s", primary_exc)
                # Primary stage is disposable; fallback begins in its own stage.
        count, size, fmt = download_with_archive_fallback(
            target, destination, timeout=args.timeout, token=token,
            max_download=max_download, max_extract=max_extract, max_files=args.max_files,
            max_depth=args.max_depth, keep_archive=args.keep_archive,
            no_overwrite=args.no_overwrite)
        LOG.info("SUCCESS: downloaded %d file(s), %.2f MiB using %s archive fallback.",
                 count, size / (1024 * 1024), fmt)
        return 0
    except DownloadError as exc:
        LOG.error("%s", exc)
        return 1
    except KeyboardInterrupt:
        LOG.error("Interrupted.")
        return 130
    except Exception:
        LOG.exception("Unexpected error.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
```

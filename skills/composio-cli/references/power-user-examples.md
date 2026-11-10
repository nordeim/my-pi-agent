# Power-User Examples

Load this file when the user needs more than one top-level command or wants to script workflows with `composio run`.

## Use `run` To Chain Tool Calls

Fetch from multiple connected tools in one script:

If the user does not need script logic and just wants a few independent calls, prefer top-level parallel execute instead:

```bash
composio run '
  const me = await execute("GITHUB_GET_THE_AUTHENTICATED_USER");
  const emails = await execute("GMAIL_FETCH_EMAILS", {
    max_results: 2,
  });

  console.log({
    login: me.data.login,
    emailCount: Array.isArray(emails.data?.messages) ? emails.data.messages.length : null,
  });
'
```

```bash
composio execute --parallel \
  GMAIL_FETCH_EMAILS -d '{ max_results: 2 }' \
  GITHUB_GET_THE_AUTHENTICATED_USER -d '{}'
```

## Use `Promise.all` To Fan Out

Fetch from multiple services at once:

```bash
composio run '
  const [me, emails] = await Promise.all([
    execute("GITHUB_GET_THE_AUTHENTICATED_USER"),
    execute("GMAIL_FETCH_EMAILS", { max_results: 5 }),
  ]);

  console.log({
    login: me.data.login,
    emailCount: emails.data.messages?.length ?? null,
  });
'
```

## Use `search()` Before `execute()` Inside A Script

Discover a candidate slug, then execute it:

Batch related discovery work with multiple queries when it keeps the workflow simpler:

```bash
composio run '
  const results = await search("get the authenticated github user", {
    toolkits: "github",
    limit: 1,
  });

  const slug = results.results?.[0]?.primary_tool_slugs?.[0];
  if (!slug) throw new Error("No candidate tool found.");

  const output = await execute(slug);

  console.log(output.data.login);
'
```

```bash
composio search "send an email" "create a github issue" --toolkits gmail,github
```

## Use `proxy()` For Raw API Access

`proxy(toolkit)` returns a fetch-compatible function bound to the connected account. Name it like `fetch` if that keeps the script clearer. It returns a real `Response`, so call `.json()` or `.text()`.

```bash
composio run '
  const fetch = await proxy("github");
  const profile = await (await fetch("https://api.github.com/user")).json();
  console.log(profile);
'
```

## Mix `execute()` And `proxy()`

Use dedicated tools where they exist, then drop down to raw API calls for the missing step:

```bash
composio run '
  const me = await execute("GITHUB_GET_THE_AUTHENTICATED_USER");

  const fetch = await proxy("github");
  const repos = await (await fetch("https://api.github.com/user/repos?per_page=3")).json();

  console.log({
    login: me.data.login,
    repoCount: Array.isArray(repos) ? repos.length : null,
  });
'
```

## Use `run` Flags Intentionally

- Use `--dry-run` to preview every `execute()` call in the script.

- Use `--debug` to see helper steps while the script runs.

Example:

```bash
composio run --dry-run --debug 'await execute("GITHUB_CREATE_AN_ISSUE", { owner: "acme", repo: "app", title: "Bug report", body: "Steps to reproduce..." })'
```

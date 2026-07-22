**1. Next.js 16 params API (async/await for params)**

*Claim validated.* Next.js 16 requires `params` and `searchParams` to be awaited. In Next.js 15 they became Promises; Next.js 16 fully removes synchronous access. Using old synchronous patterns results in `undefined` or errors.

**Recommended fix:** Make page/layout components `async` and `await` the `params` prop. For TypeScript, type `params` as `Promise<{ slug: string }>`. For client components, use React’s `use()` hook: `const resolvedParams = use(params)`. Run the official codemod: `npx @next/codemod@latest migrate-to-async-dynamic-apis`.

---

**2. React 19 JSX.Element**

*Claim validated.* React 19 removed the global `JSX` namespace, so `JSX.Element` is deprecated and causes TypeScript errors.

**Recommended fix:** Use `React.ReactElement` (or `ReactElement`) as the return type, e.g., `export function MyComponent(): ReactElement { ... }`. Alternatively, use `React.JSX.Element`. The cleanest approach for function components is to **omit the return type entirely** and let TypeScript infer it.

---

**3. window.location.href vs useRouter()**

*Claim validated.* Using `window.location.href` causes a full page reload, destroys client‑side state (React Query cache, scroll position), and disrupts the SPA experience. It also introduces potential XSS risks.

**Recommended fix:** For programmatic navigation, use `useRouter` from `next/navigation`: `router.push('/target')` or `router.replace('/target')`. For declarative navigation, use the `<Link>` component.

---

**4. `<a>` vs `<Link>`**

*Claim validated.* Standard `<a>` tags trigger full page reloads. The Next.js `<Link>` component provides client‑side navigation, automatic prefetching, and better performance.

**Recommended fix:** Replace internal `<a href="...">` with `<Link href="...">` imported from `next/link`. Use `<a>` only for external links or when you specifically need a full page reload.

---

**5. Emojis**

*Claim validated.* Raw emojis cause inconsistent cross‑platform rendering, lack styling control, and create accessibility gaps—screen readers may mispronounce or skip them.

**Recommended fix (Option A — icon library):** Replace emojis with SVG icons from `lucide-react` (or similar) for consistent rendering, theme support, and built‑in accessibility.

**Recommended fix (Option B — accessible emoji):** Wrap emojis in `<span role="img" aria-label="description">emoji</span>` so screen readers announce them properly. Add `aria-hidden="true"` for purely decorative emojis.

---

**6. useOptimistic Misuse**

*Claim validated.* `useOptimistic` is designed for async operations where the UI should reflect a pending state before the server confirms. For a simple boolean toggle that doesn’t involve an async server action, `useOptimistic` is unnecessary overhead.

**Recommended fix:** Replace with `useState`. Example:
```tsx
const [isWishlisted, setIsWishlisted] = useState(false);
const handleToggle = () => setIsWishlisted(prev => !prev);
```
If an async server action *is* involved (e.g., saving to DB), `useOptimistic` is appropriate. Then wrap the dispatch in `startTransition` and ensure errors are thrown (not returned) so automatic rollback works.

---

**7. async on RSCs**

*Claim validated.* Marking a Server Component `async` when it performs no `await` is unnecessary and can introduce subtle overhead.

**Recommended fix:** Remove the `async` keyword from any Server Component or function that doesn’t use `await`. Only declare a component `async` when it actually performs asynchronous work (data fetching, `await params`, etc.).

---

### Summary Table

| Issue | Validated | Recommended Fix |
|-------|-----------|-----------------|
| 1. Next.js 16 params API | ✅ Yes | `async` page → `await params`; type as `Promise<{...}>`; or `use(params)` in client components |
| 2. React 19 JSX.Element | ✅ Yes | Replace with `React.ReactElement` or omit return type |
| 3. window.location.href | ✅ Yes | Use `useRouter().push()` or `<Link>` |
| 4. `<a>` vs `<Link>` | ✅ Yes | Use `<Link>` for internal navigation |
| 5. Emojis | ✅ Yes | Replace with Lucide icons or wrap in `<span role="img" aria-label="...">` |
| 6. useOptimistic Misuse | ✅ Yes | Use `useState` for simple toggles; `useOptimistic` only with async server actions |
| 7. async on RSCs | ✅ Yes | Remove `async` from components with no `await` |

# https://chat.deepseek.com/share/8f7d3zb53kgi1rtc15 


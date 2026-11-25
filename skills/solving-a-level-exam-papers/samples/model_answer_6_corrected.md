# ACJC 2026 JC2 Preliminary Examination — H2 Further Mathematics 9649/01
## Question 6 — Unified Model Answer (v2, corrected) · Total 10 marks

> **Cover rules (verbatim):** "Give non-exact numerical answers correct to
> 3 significant figures, or 1 decimal place in the case of angles in degrees,
> unless a different level of accuracy is specified in the question."
> Unsupported GC answers are allowed unless a question states otherwise.

---

## 0. Source and transcription note

The pasted question was damaged by PDF text extraction (modulus bars and conjugate asterisks were lost). The statement below is reconstructed from the paper (p.4) and cross-checked against the **official solutions bound into the same PDF**.

| Item | Status |
|---|---|
| Mathematical content (circle $5i$, $3\sqrt2$; $\tfrac{3\pi}{4}-\sin^{-1}\tfrac13$; $\theta=\sin^{-1}\tfrac{3\sqrt2}{5}$; $\lvert w\rvert=\sqrt7$) | **Verified** — matches the official solutions |
| Typeset form $\left\lvert\frac{w-a^*}{w+a^*}\right\rvert=1$ | **Reasoned** — inferred from the extracted `* * … = 1` pattern and confirmed by the solution's first step $\lvert w-a^*\rvert=\lvert w+a^*\rvert$ |
| Per-step mark allocations in §6 | **Reasoned / indicative** — the PDF contains solutions, not a mark scheme |

> **Note on the factor 3:** it is $3$ in the question; it becomes $9$ **when squared**. Nothing else changes.

---

## 1. The question

In an Argand diagram, $P$ represents $z$ satisfying
$$|z-9+4i|=3|z-1-4i|.$$
Let the locus of $P$ be the curve $C$.

**(a)** By letting $z=x+iy$ and finding the Cartesian equation of $C$, show that $C$ is a circle, and state its centre and radius. **[3]**

**(b)** Find the exact minimum value of $\arg(z-9+4i)$. **[2]**

A given complex number $a$ with $0<\arg a<\tfrac{\pi}{2}$ has the property that there is **exactly one** complex number $w$ satisfying
$$|w-9+4i|=3|w-1-4i| \qquad\text{and}\qquad \left|\frac{w-a^*}{w+a^*}\right|=1 .$$

**(c)** Find all possible value(s) of $a$, and state the corresponding value(s) of $w$. **[5]**

---

## 2. Strategy

All three parts concern **the same circle**.

| Part | Concept | Method |
|---|---|---|
| (a) | Locus of a complex number | Cartesian expansion → completing the square |
| (b) | $\arg\big(z-(9-4i)\big)$ = direction of $\overrightarrow{AP}$ | Tangents from an **external point** $A(9,-4)$ |
| (c) | Equal moduli ⇒ perpendicular bisector | Line **tangent** to $C$ ⇒ exactly one intersection |

**Notation used throughout:** $O$ = origin, $C=(0,5)$ = centre of the circle, $A=(9,-4)$.

---

## 3. Worked solution

### (a) Cartesian equation, centre and radius [3]

Let $z=x+iy$, $x,y\in\mathbb{R}$. Then
$$|(x-9)+(y+4)i|=3\,|(x-1)+(y-4)i|.$$

Squaring both sides (using $|p+qi|^2=p^2+q^2$):
$$(x-9)^2+(y+4)^2=9\big[(x-1)^2+(y-4)^2\big]$$
$$x^2-18x+81+y^2+8y+16=9x^2-18x+9+9y^2-72y+144$$
$$8x^2+8y^2-80y+56=0$$
$$\boxed{\,x^2+y^2-10y+7=0\,}$$

Completing the square:
$$x^2+(y-5)^2-25+7=0\qquad\Longrightarrow\qquad \boxed{\,x^2+(y-5)^2=18\,}$$

This is of the form $(x-h)^2+(y-k)^2=r^2$ with $r^2=18>0$, **so $C$ is a circle**, with

$$\textbf{centre } (0,5)\ \ (\text{i.e. } 5i),\qquad \textbf{radius } \sqrt{18}=3\sqrt2 .$$

---

### (b) Exact minimum of $\arg(z-9+4i)$ [2]

**Step 1 — Interpret.** Since $z-9+4i=z-(9-4i)$, the quantity $\arg(z-9+4i)$ is the angle that $\overrightarrow{AP}$ makes with the positive real direction, where $A$ represents $9-4i$, i.e. $A=(9,-4)$.

**Step 2 — Locate $A$ relative to $C$.**
$$\overrightarrow{AC}=5i-(9-4i)=-9+9i,\qquad |AC|=\sqrt{81+81}=9\sqrt2 .$$
Since $9\sqrt2>3\sqrt2$, **$A$ lies outside $C$**, so two tangents exist and the extreme arguments occur at the tangency points.

Because $\overrightarrow{AC}=-9+9i$ has **negative real part and positive imaginary part**, it points into the second quadrant with reference angle $\tan^{-1}\tfrac99=\tfrac{\pi}{4}$:
$$\arg\overrightarrow{AC}=\pi-\frac{\pi}{4}=\frac{3\pi}{4}.$$

**Step 3 — Tangent geometry.** Let $T$ be a point of tangency. Then $CT\perp AT$, so in right-angled $\triangle ACT$,
$$\sin\alpha=\frac{CT}{AC}=\frac{3\sqrt2}{9\sqrt2}=\frac13,\qquad \alpha=\angle TAC=\sin^{-1}\!\frac13 .$$

**Step 4 — Choose the minimum.** The two tangent directions have arguments $\dfrac{3\pi}{4}\pm\alpha$; the **smaller** is obtained by subtracting:

$$\boxed{\ \min\arg(z-9+4i)=\frac{3\pi}{4}-\sin^{-1}\!\left(\frac13\right)\ }$$

*Principal-value check:* $\sin\alpha=\tfrac13<\tfrac{1}{\sqrt2}\Rightarrow\alpha<\tfrac{\pi}{4}$, so both $\tfrac{3\pi}{4}\pm\alpha\in\left(\tfrac{\pi}{2},\pi\right)$ — no branch wrap-around.

**Figure 1** (schematic, not to scale; second tangent omitted for clarity)

```
                      y
                      │
             .────────┼────────.
           ╱          │          ╲
          │           │           │ ● T₁  ← tangency giving MINIMUM arg
          │         C ●           │  ╲
          │        (0,5)          │   ╲   tangent AT₁
           ╲          │          ╱     ╲
             '────────┼────────'        ╲
                      │                  ╲
   ───────────────────O───────────────────╲──────→ x
                      │                    ● A(9,−4)
```

| Element | Exact value |
|---|---|
| Centre $C$ / radius | $(0,5)$ / $3\sqrt2$ |
| $A$ | $(9,-4)$ |
| $\lvert AC\rvert$ / tangent length $AT$ | $9\sqrt2$ / $\sqrt{162-18}=12$ |
| $T_1$ (min arg) | $\big(1+2\sqrt2,\;4+2\sqrt2\big)$ |
| $T_2$ (max arg) | $\big(1-2\sqrt2,\;4-2\sqrt2\big)$ |

---

### (c) All possible $a$, and the corresponding $w$ [5]

**Step 1 — The second condition is a straight line.**
$$\left|\frac{w-a^*}{w+a^*}\right|=1\iff |w-a^*|=|w+a^*|=|w-(-a^*)|\quad (w\neq -a^*),$$
so $w$ is equidistant from $a^*$ and $-a^*$: **$w$ lies on the perpendicular bisector $\ell$ of the segment joining $a^*$ and $-a^*$.** Its midpoint is $O$, so $\ell$ passes through the origin.

**Step 2 — Cartesian equation of $\ell$.** Let
$$a=\rho(\cos\theta+i\sin\theta),\quad \rho>0,\ \ 0<\theta<\tfrac{\pi}{2},\qquad w=u+iv .$$
Squaring $|w-a^*|=|w+a^*|$:
$$(w-a^*)(w^*-a)=(w+a^*)(w^*+a)$$
$$ww^*-wa-a^*w^*+aa^*=ww^*+wa+a^*w^*+aa^*$$
$$\Rightarrow\ wa+a^*w^*=0\ \Rightarrow\ 2\operatorname{Re}(wa)=0\ \Rightarrow\ \operatorname{Re}(wa)=0 .$$
Substituting and using $\rho>0$:
$$\rho\,(u\cos\theta-v\sin\theta)=0\qquad\Longrightarrow\qquad \boxed{\,\ell:\ u\cos\theta-v\sin\theta=0\,}$$

$\ell$ passes through $O$ with unit normal $\mathbf n=(\cos\theta,-\sin\theta)$, gradient $\cot\theta>0$, and direction angle $\tfrac{\pi}{2}-\theta\in\left(0,\tfrac{\pi}{2}\right)$.

**Step 3 — "Exactly one $w$" ⇒ tangency.** From (a), the first condition is the circle $u^2+(v-5)^2=18$. A line meets a circle in $0$, $1$ or $2$ points, and **exactly one only when it is tangent**. Hence
$$\operatorname{dist}\big(C,\ell\big)=\frac{|0\cdot\cos\theta-5\sin\theta|}{\sqrt{\cos^2\theta+\sin^2\theta}}=5\sin\theta=3\sqrt2\quad(\sin\theta>0),$$
$$\boxed{\ \sin\theta=\frac{3\sqrt2}{5}\ },\qquad \cos\theta=\sqrt{1-\frac{18}{25}}=\frac{\sqrt7}{5},\qquad \boxed{\ \theta=\sin^{-1}\!\frac{3\sqrt2}{5}\ }.$$

*Uniqueness:* $\tfrac{3\sqrt2}{5}<1$ and $\sin$ is strictly increasing on $\left(0,\tfrac{\pi}{2}\right)$, so $\theta$ is unique. The two tangents from $O$ to $C$ have gradients $\pm\tfrac{\sqrt{14}}{6}$; since $\cot\theta>0$, only the **positive-gradient** tangent is admissible — the other would require $\theta=\pi-\sin^{-1}\tfrac{3\sqrt2}{5}\notin\left(0,\tfrac{\pi}{2}\right)$ and is **rejected**.

**Step 4 — All possible $a$.** Only $\arg a$ is fixed; $|a|$ is free:
$$\boxed{\ a=r\,e^{i\theta}=r\left(\frac{\sqrt7}{5}+\frac{3\sqrt2}{5}i\right),\quad \theta=\sin^{-1}\!\frac{3\sqrt2}{5},\quad \text{for every } r>0\ }$$
i.e. **infinitely many** $a$, all on one ray from $O$ (excluding $O$).

**Step 5 — The corresponding $w$ (point of tangency).** Since $Ow\perp Cw$,
$$|w|=\sqrt{|OC|^2-r_{\text{circle}}^2}=\sqrt{25-18}=\sqrt7 .$$
$C$ lies wholly in the upper half-plane ($5-3\sqrt2>0$), so $v>0$ and $\arg w=\tfrac{\pi}{2}-\theta$. Hence
$$\boxed{\ w=\sqrt7\,e^{\,i\left(\frac{\pi}{2}-\sin^{-1}\frac{3\sqrt2}{5}\right)}=\frac{3\sqrt{14}}{5}+\frac75 i\ }$$
using $\cos\!\left(\tfrac{\pi}{2}-\theta\right)=\sin\theta=\tfrac{3\sqrt2}{5}$ and $\sin\!\left(\tfrac{\pi}{2}-\theta\right)=\cos\theta=\tfrac{\sqrt7}{5}$.

*Equivalent exact forms:* $\arg w=\cos^{-1}\tfrac{3\sqrt2}{5}$ (identity $\cos^{-1}x=\tfrac{\pi}{2}-\sin^{-1}x$).
*Denominator check:* $\arg w\in\left(0,\tfrac{\pi}{2}\right)$ while $\arg(-a^*)=\pi-\theta\in\left(\tfrac{\pi}{2},\pi\right)$, so $w\neq-a^*$ and the fraction is defined. ✔

**Every admissible $a$ gives the same unique $w$**, because $\ell$ depends only on $\theta$, not on $r$.

**Step 6 — Algebraic cross-check of $w$ (projection).** With $\mathbf n=(\cos\theta,-\sin\theta)$ and $C\cdot\mathbf n=-5\sin\theta$, the foot of the perpendicular from $C$ to $\ell$ is
$$\overrightarrow{OT}=\overrightarrow{OC}-(C\cdot\mathbf n)\mathbf n=(0,5)+5\sin\theta(\cos\theta,-\sin\theta)=\big(5\sin\theta\cos\theta,\;5\cos^2\theta\big)=\left(\frac{3\sqrt{14}}{5},\frac75\right).\ ✔$$

**Figure 2** (schematic, not to scale)

```
   Panel A: the bisector                Panel B: tangency to C
              y                                    y
              │                                    │
   −a* ●      │        ↗ ℓ                  .──────┼──────.
          ╲   │    ↗                      ╱        │        ╲
            ╲ │ ↗   direction π/2 − θ    │       C ●         │
   ──────────╲O──────────→ x             │      (0,5)        │
              │╲                          ╲        │        ╱
              │  ╲                          '──────┼───●──'   ● w = (3√14/5, 7/5)
              │    ● a*  (arg −θ)                │  ╱
                                          ───────O──────────────→ x
                                               ╱ │   ℓ : u cos θ − v sin θ = 0
```

| Element | Exact value |
|---|---|
| $\theta=\arg a$ | $\sin^{-1}\tfrac{3\sqrt2}{5}$ |
| Direction of $\ell$ | $\tfrac{\pi}{2}-\theta$; gradient $\cot\theta=\tfrac{\sqrt{14}}{6}$ |
| $w$ | $\left(\tfrac{3\sqrt{14}}{5},\tfrac75\right)$, $\lvert w\rvert=\sqrt7$ |

---

## 4. Answer summary (booklet-ready)

| Part | Answer |
|---|---|
| (a) Cartesian equation | $x^2+y^2-10y+7=0$, i.e. $x^2+(y-5)^2=18$ — a circle |
| (a) Centre / radius | $(0,5)$ (i.e. $5i$) / $3\sqrt2$ |
| (b) Minimum argument | $\dfrac{3\pi}{4}-\sin^{-1}\!\left(\dfrac13\right)$ |
| (c) All possible $a$ | $a=r\,e^{i\sin^{-1}(3\sqrt2/5)}=\dfrac{r}{5}\left(\sqrt7+3\sqrt2\,i\right)$, **any** $r>0$ |
| (c) Corresponding $w$ | $w=\sqrt7\,e^{i\left(\frac{\pi}{2}-\sin^{-1}\frac{3\sqrt2}{5}\right)}=\dfrac{3\sqrt{14}}{5}+\dfrac75 i$ (same for every such $a$) |

---

## 5. Verification ledger

Rows 1–10 are exact hand algebra shown in full; rows 11–12 are labelled **Reasoned**. Independently, the seven checks in `assets/checks.example.json` were **executed** with `scripts/check_math.py` (they cover rows 2–6 and the two domain intervals, cf. row 9): 7/7 PASS, exit 0.

| Provenance | Value |
|---|---|
| `checks_sha256` | `18c1a7f6668c01f2…` |
| Tool versions | sympy 1.14.0 · Python 3.11.2 |

Decimals are indicative sanity values only, not exam answers.

| # | Check | Evidence | Status |
|---|---|---|---|
| 1 | Circle equation | $8x^2+8y^2-80y+56=0\Rightarrow x^2+(y-5)^2=18$ | **Verified** |
| 2 | $w$ lies on $C$ | $\left(\tfrac{3\sqrt{14}}5\right)^2+\left(\tfrac75-5\right)^2=\tfrac{126+324}{25}=18$ | **Verified** |
| 3 | $w$ satisfies the **original** modulus equation | $\lvert w-9+4i\rvert^2=\tfrac{2880-270\sqrt{14}}{25}=9\cdot\tfrac{320-30\sqrt{14}}{25}=9\lvert w-1-4i\rvert^2$ | **Verified** |
| 4 | $w$ satisfies $\operatorname{Re}(wa)=0$ | $\tfrac{3\sqrt{14}}5\sqrt7-\tfrac75\cdot3\sqrt2=\tfrac{21\sqrt2-21\sqrt2}{5}=0$ | **Verified** |
| 5 | $\lvert w\rvert$ agrees with official key | $\tfrac{126+49}{25}=7\Rightarrow\lvert w\rvert=\sqrt7$ | **Verified** |
| 6 | Tangency ⇒ **exactly one** $w$ | $v=\tfrac{\sqrt{14}}6u$ into $C$: $25u^2-30\sqrt{14}u+126=0$, $\Delta=12600-12600=0$ | **Verified** |
| 7 | Fraction defined | $w\neq-a^*$ (arguments in disjoint quadrants) | **Verified** |
| 8 | (b) tangency point exact | $T_1=(1+2\sqrt2,4+2\sqrt2)$: $(9+4\sqrt2)+(9-4\sqrt2)=18$ ✔ on $C$ | **Verified** |
| 9 | Principal-argument safety | $\sin\alpha=\tfrac13<\tfrac1{\sqrt2}\Rightarrow\tfrac{3\pi}4\pm\alpha\in(\tfrac\pi2,\pi)$ | **Verified** |
| 10 | Second tangent excluded | Tangents from $O$: gradients $\pm\tfrac{\sqrt{14}}6$; $\cot\theta>0$ | **Verified** |
| 11 | Printed typography of the (c) condition | Only extracted text available | **Reasoned** |
| 12 | Per-step mark splits (§6) | No mark scheme in the PDF | **Reasoned** |

*Indicative decimals:* $\min\arg\approx2.016$; $\theta\approx1.011$; $w\approx2.245+1.400i$; $\lvert w\rvert\approx2.646$.

---

## 6. Examiner-facing notes

**Indicative credit** — (a): squaring/expansion, completing the square, centre **and** radius. (b): tangent-from-external-point geometry, exact answer. (c): perpendicular bisector, line equation, tangency condition, $\theta$, then $a$ **and** $w$.

**Common errors to avoid**
1. Squaring $3|z-1-4i|$ as $3(\dots)$ instead of $9(\dots)$.
2. Measuring $\arg(z-9+4i)$ from the **origin** instead of from $A(9,-4)$.
3. **Adding** $\alpha$ (that gives the maximum), or forgetting the principal-value check.
4. Assuming $a$ is unique — the modulus of $a$ is unrestricted.
5. Offering the second tangent $\theta=\pi-\sin^{-1}\tfrac{3\sqrt2}{5}$, which violates $0<\arg a<\tfrac\pi2$.
6. Using $O$ for the centre (reserve $O$ for the origin; use $C$).
7. Giving decimals where exact surd/inverse-trig forms are expected.

---

## 7. Change log (audit closure)

| Audit ID | Resolution in v2 |
|---|---|
| MAJ-1 | External image/links removed; self-contained labelled schematics + exact coordinate tables added |
| MIN-1 | $3\pi/4$ justified from the components of $\overrightarrow{AC}=-9+9i$ |
| MIN-2 | Rewritten as "the two tangent directions are $3\pi/4\pm\alpha$" |
| MIN-3 | $x^2+(y-5)^2=18$ displayed; "so $C$ is a circle" stated |
| MIN-4 | $C$ = centre, $O$ = origin; $\overrightarrow{OT}$ / $\overrightarrow{CT}$ used correctly |
| MIN-5 | Bogus "$3$ not $3^2$" correction deleted; replaced by a correct squaring note |
| MIN-6 | Transcription and mark-splits explicitly labelled **Reasoned** |
| SELF-1/2 | Fraction form adopted as primary; $\cos^{-1}$ form labelled as an identity |
| SELF-3 | Problem-specific figures supplied (schematic + exact coordinates) |
| ENH-1…5 | $A$ outside $C$; second tangent rejected; polar forms and $\lvert w\rvert=\sqrt7$; full verification; $w\neq-a^*$ |

---

## Handoff
**Verified:** 7/7 exact checks executed via `assets/checks.example.json`
(`checks_sha256=18c1a7f6668c01f2…`, sympy 1.14.0): original modulus equation,
circle membership, equal-distance line, tangency discriminant, |w|=√7, both
domain intervals. Ledger rows 1, 7, 8 and 10 are hand algebra only (not machine-checked).
**Deferred:** figures are ASCII schematics, not vector graphics; per-step mark
splits are indicative (the PDF carries solutions, not a mark scheme); the
typeset form of the fraction condition is a reconstruction from extraction.

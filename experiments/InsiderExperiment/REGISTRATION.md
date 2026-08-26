# REGISTRATION

InsiderExperiment. A net-of-cost survival test on Form 4 insider purchases.

Registered 2026-08-25, Stage A.1. Every parameter in this document is fixed
before any measurement runs. Section 0 is committed before Task 4 computes
anything, so the answer cannot be read against a threshold its own measurement
could see. Changing a registered value after that commit requires a numbered
amendment in Section 17 carrying its own evidence.

---

## Section 0. The gates

Two gates fire in Stage A.1. Neither reads a first moment. The corpus gate reads
counts. The power gate reads a minimum detectable effect, which is built from a
dispersion and a sample size and from nothing else.

### 0.1 Why this section exists

NPDExperiment closed at unresolved-at-achievable-power. Its realized minimum
detectable contrast came in at 0.0512 against a realistic effect band of 0.01 to
0.05, so the design could not have detected an effect anywhere in the range the
literature reports. That was discovered after 415 days of collection and 6.9378
USD of spend, in the same session that read the result. Its ADR-007 had
registered the risk in advance and the arithmetic still landed too late to
change anything.

The separation that makes an earlier answer possible: alpha is a first moment,
detectability is a second moment. The minimum detectable effect depends on the
portfolio's tracking error and its effective number of independent periods, and
neither requires knowing the mean.

### 0.2 The power gate

Fired on the minimum detectable monthly alpha for the primary calendar-time
portfolio at the registered six-month hold, value-weighted, at t 2.0.

| Verdict | Bar | Consequence |
|---|---|---|
| **GO** | MDE at or below 20 bp per month | The design can resolve the decayed effect band with margin. Stage B is authorized. |
| **DEGRADED** | MDE between 20 and 40 bp per month | The design can resolve the top of the decayed gross band but likely not the net residual after 32 to 100 bp round trip. Stage B is authorized only if the registration records, before B runs, that a gross-detectable net-undetectable outcome is a registered verdict row and not a disappointment. |
| **BLOCKED** | MDE above 40 bp per month | The design cannot detect an effect anywhere in the range the literature reports. Stage B is never written and the repo closes on the finding. |

Boundaries are inclusive at the lower edge. An MDE of exactly 20.00 bp is GO. An
MDE of exactly 40.00 bp is DEGRADED.

The bars are set against the decayed effect band, not the original one. Cohen,
Malloy and Pomorski report 82 bp per month value-weighted on opportunistic
purchases over 1989 to 2007. That replicates at roughly 30 to 40 bp per month on
2008 to 2024 data, a 60 to 70 percent decay. Ozlen and Batumoglu (SSRN 5966834,
December 2025, Russell 2000 Form 4) report 70 to 80 percent of total alpha
dissipating between the transaction date and the following trading day, before a
public filer can act, leaving a residual they describe as largely confirmatory
rather than informative.

The 20 bp GO bar sits below the bottom of the decayed gross band, so a GO design
resolves the whole band. The 40 bp BLOCKED bar sits at the top of it, so a design
above 40 bp cannot resolve any part of the band.

### 0.3 The corpus gate

| Verdict | Bar |
|---|---|
| **CORPUS-GO** | The EDGAR pipeline builds and qualifying events exceed the registered floor. |
| **CORPUS-BLOCKED** | EDGAR access fails, or qualifying events fall below the floor after the ex-ante filters. Record and stop. |

Registered floor, both conditions required:

- **1,000 qualifying events** over the bar span, counted after every ex-ante
  filter in Section 3.
- **80 percent of in-span sessions carrying a non-empty book** at the primary
  six-month hold.

### 0.4 How the qualifying-event floor was derived

The binding constraint is not the raw filing count. It is the number of
independent calendar periods and the portfolio's tracking error. The event count
enters only through book width, and book width enters only through tracking
error.

Write the minimum detectable monthly alpha as

    MDE_month = t * M * s_d / sqrt(N_eff)

with t the critical value 2.0, M the registered 21 sessions per month, s_d the
daily excess-return standard deviation, and N_eff the effective independent
period count after the serial-correlation penalty.

Take the planning figures fixed here: N of 2,520 daily observations over the
ten-year bar span and a variance inflation factor of 1.5, so N_eff is 1,680 and
sqrt(N_eff) is 40.99. Both are planning values. The realized N and the realized
inflation factor are measured in Task 5 and reported beside these.

Invert the expression at each bar:

| Bar | Daily excess-return SD | Annualized tracking error |
|---|---|---|
| 20 bp per month, the GO ceiling | 19.52 bp | 3.10 percent |
| 40 bp per month, the BLOCKED floor | 39.04 bp | 6.20 percent |

So the design stays out of BLOCKED as long as annualized tracking error is at or
below about 6.2 percent, and reaches GO at or below about 3.1 percent.

Now convert tracking error into book width. For a book of k names with average
idiosyncratic volatility sigma and residuals close to independent, tracking
error is about sigma over sqrt(k). Taking sigma at 30 percent annualized, which
is a standard figure for the liquid band this universe covers:

| Bar | Required book width k |
|---|---|
| 6.2 percent tracking error, the BLOCKED floor | 23.4 names |
| 3.1 percent tracking error, the GO ceiling | 93.7 names |

Now convert book width into event count. At a hold of H sessions and a steady
arrival of lambda qualifying events per session, expected book width is H times
lambda when no two events name the same issuer. At H of 126 sessions:

| Book width k | Events per session | Events over 2,520 sessions |
|---|---|---|
| 23.4, the BLOCKED floor | 0.186 | 468 |
| 50, the registered floor | 0.397 | 1,000 |
| 93.7, the GO ceiling | 0.744 | 1,875 |

**The floor is set at 1,000 qualifying events**, which is a book of about 50
names. Three reasons for placing it above the 468 that BLOCKED alone requires.

First, the H times lambda identity assumes distinct issuers. Insider purchases
cluster in the same name, and cluster buys are by construction three or more
filers at one issuer, so realized distinct-issuer width is below the arrival
count. The margin absorbs that.

Second, arrival is not steady. Insider purchases concentrate after price declines
and around earnings windows, so a book that averages 50 names will be thinner
than 24 on some stretches, and those stretches carry the variance.

Third, at 1,000 events the expected tracking error is about 4.24 percent and the
expected MDE about 27 bp per month, which sits inside DEGRADED with room on both
sides. A floor placed at the BLOCKED boundary would admit corpora whose verdict
was decided by rounding.

The coverage floor of 80 percent follows from the same expression. N enters as a
square root, so dropping from 2,520 to 2,016 sessions raises the MDE by 11.8
percent, which is tolerable. Below that the penalty compounds, and more to the
point a book that is empty on more than one day in five is not a calendar-time
portfolio.

### 0.5 What fires these gates

`insider.section0.fire_power_gate` and `insider.section0.fire_corpus_gate`. The
bars live in `insider.config.CONFIG` as `mde_go_ceiling_bp`,
`mde_degraded_ceiling_bp`, `corpus_event_floor` and `corpus_coverage_floor`, and
`tests/test_guards.py` fails if any of them has no enforcement site.

Neither function can read a realized return. `insider.power` takes its input from
`var/insider_dispersion.db`, which holds daily portfolio excess returns already
centered on their own mean. The mean is never written there, so it cannot be
recovered. The raw series lives in `var/insider_sealed.db` and
`insider.eval.evaluator` is its only permitted reader.

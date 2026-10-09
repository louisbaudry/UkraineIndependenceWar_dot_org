# Verification record — regional administration Telegram channels (DR-0109 step 2)

**Status:** Verification record for six candidate registrations. Nothing here
is registered, nothing is collected into the project's archive, and nothing is
enacted by this document. Registering any one candidate is the founder's act,
per source, on the archive server (DR-0067, DR-0093 §3); no Decision Record
acts on this yet. **AI provenance (record §80):** drafted by an AI assistant
(Anthropic Claude Code agent session); nothing has been reviewed by the founder.
**Verified:** 2026-10-09, from a session.
**Candidates:** the six `ua-oda-*-telegram` keys in
[`sources/candidates/civilian-harm.yaml`](../../sources/candidates/civilian-harm.yaml).
**Mandate:** [DR-0109](../decision-records/DR-0109-civilian-harm-and-memorial.md)
Decision 5, step 2 ("regional administration (oblast) Telegram channels —
per-incident reports"), issue #61. DR-0109 sizes step 2 at about two dozen
channels and says it is weighed against the suspension of collection at scale
(DR-0072) when put to the founder. Six of about two dozen are verified here;
the rest are not.

## 1. Why every handle needs its provenance

Telegram handles are first-come. Guessing "the obvious handle" for an
administration found impostors and dead channels within the first batch (§3), so
a handle is accepted only if the **administration's own website links to it**.

## 2. Method

1. 40 plausible handles for the oblast administrations were requested from
   `t.me/s/<handle>` (Telegram's public preview), one request every 1.5 s. A
   handle counts as a channel only if the page carries a channel header.
2. For each oblast whose official site could be reached, the front page was
   fetched and searched for `t.me/` links.
3. For each channel confirmed that way, the visible posts were counted, and
   scanned for strike/casualty vocabulary and for age-like victim detail
   (Ukrainian "N-річний/річна", "чоловік/жінка N років"). **Counts only**; no
   post text is quoted here or saved.

Not done: no channel was rehearsed through the collector; photographs and
videos were not inspected; no history was paged.

## 3. Result

### Confirmed by the administration's own site

| Oblast | Site (200) | Channel | Posts visible | Strike/casualty vocabulary | Age-like victim detail |
|---|---|---|---|---|---|
| Kharkiv | `kharkivoda.gov.ua` | `kharkivoda` | 12 | 5 | 0 |
| Kherson | `khoda.gov.ua` | `khersonskaODA` | 7 | 4 | 2 |
| Zaporizhzhia | `zoda.gov.ua` | `zoda_gov_ua` | 8 | 8 | 1 |
| Kyiv Oblast | `koda.gov.ua` | `kyivoda` | 20 | 13 | 0 |
| Poltava | `poda.gov.ua` | `poltavskaoda` (same as `poltavskaODA`) | 11 | 3 | 0 |
| Vinnytsia | `vin.gov.ua` | `VinnytsiaODA` | 17 | 6 | 0 |

The Kharkiv site also links `synegubov`, whose description calls it the head of
the administration's official channel. That is a person's channel, not the
administration's, so it is left out of the candidates; whether to add it is the
founder's call.

### Rejected or unconfirmed

- `mykolaivskaODA`: description reads "channel for sale" with an advertising
  contact, 306 subscribers, one visible post from March. **Not the
  administration's.** The Mykolaiv site (`mk.gov.ua`, 200) carries no Telegram
  link, so the real channel is not established.
- `sumy_oda`: a Russian-language channel ("Sumy — Russia"), one post. **An
  impostor.** `kherson_oda` (one post, 2023) and `kyivregion` (15 subscribers,
  last post 2020) are dead lookalikes.
- Channels that exist and look official but whose administration site could not
  be reached or showed no link, so **provenance is not established**:
  `chernigivskaODA` (site 403), `dnipropetrovskaODA` (403), `odeskaODA` (site
  unreachable), `donetskaODA` (site 200, no link), `cherkaskaODA` (403),
  `kirovohradskaODA` (403), `volynskaODA` (site 200, no link). Candidates for a
  later pass from the archive server, which reaches hosts sessions cannot.
- No channel was found for Luhansk, Sumy (real), Zhytomyr, Rivne, Lviv,
  Ivano-Frankivsk, Ternopil, Zakarpattia, Chernivtsi or the Donetsk head's
  personal channel under the handles tried; the handles tried were guesses, so
  this proves nothing about whether they exist.

## 4. Things the founder should know before accepting any of them

- **Personal data.** These are news feeds, not statistics. A few visible posts
  carry age-like detail that can identify a victim. Preserving them is the
  floor; **no victim is structured as a person** (DR-0071(b), DR-0109 Decision
  4), and no name is published before the DR-0072 successor (DR-0109).
- **Graphic content.** Photographs and videos were not inspected. The candidates
  assume graphic content and so cannot default to public access (PRES-012,
  POL-0001 §5.9; `register.py --check` enforced this). They are drafted at
  `private-preservation`, a placeholder for the founder's choice.
- **Reliability.** Graded B/3: an official source reporting on its adversary,
  first reports that are often revised.
- **Rights.** Unverified, not legally reviewed (§14, POL-0001 §10).
- **Scale.** Each channel shows only the newest ~20 posts per fetch; full
  history needs a paginated crawl that the project has not built (see
  `strike-tracking.yaml`). A daily run keeps new posts and nothing earlier.
- **Impostors.** The rejected handles show the risk is real. Any registration
  must re-check that the site still links the handle.
- **Scale decision.** Six candidates is step 2 begun, not step 2 done, and
  registering any of them is collection under the DR-0072 suspension's scale
  question that DR-0109 says to put to the founder.

## 5. Not verified

Reachability from the archive server; whether the channels have changed
handle; image and video content; rights; the other ~18 oblasts.

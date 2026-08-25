# Stage A.1b: the fractional question, settled by paper order behaviour

Run 2026-08-25, 02:57 to 03:07 UTC, Monday 22:57 to 23:07 ET, market
closed. Gateway 127.0.0.1:4002, server version 187, account [paper account ID removed],
declared mode paper. Five orders of the ten-order cap used. No order
filled. The account was flat at every moment and verified flat twice.
Read-Only API verified off by behaviour: the whole-share control order
was accepted and queued, so orders were validated on their merits.

## Task 1: eligibility across the real 2026-08-03 width-20 book

All 20 names advertise fractional sizing at the contract layer.

| symbol | conId | MinSize | SizeIncrement | long name |
|---|---|---|---|---|
| SNDK | 760250490 | 0.0001 | 0.0001 | SANDISK CORP |
| AXTI | 4726868 | 0.0001 | 0.0001 | AXT INC |
| WOLF | 817815740 | 0.0001 | 0.0001 | WOLFSPEED INC |
| MU | 9939 | 0.0001 | 0.0001 | MICRON TECHNOLOGY INC |
| WDC | 13681 | 0.0001 | 0.0001 | WESTERN DIGITAL CORP |
| BE | 326398514 | 0.0001 | 0.0001 | BLOOM ENERGY CORP- A |
| MXL | 73342855 | 0.0001 | 0.0001 | MAXLINEAR INC |
| TE | 674590140 | 0.0001 | 0.0001 | T1 ENERGY INC |
| LITE | 201113895 | 0.0001 | 0.0001 | LUMENTUM HOLDINGS INC |
| INTC | 270639 | 0.0001 | 0.0001 | INTEL CORP |
| AAOI | 135423662 | 0.0001 | 0.0001 | APPLIED OPTOELECTRONICS INC |
| STX | 491932113 | 0.0001 | 0.0001 | SEAGATE TECHNOLOGY HOLDINGS |
| TSEM | 111792216 | 0.0001 | 0.0001 | TOWER SEMICONDUCTOR LTD |
| DOCN | 478483393 | 0.0001 | 0.0001 | DIGITALOCEAN HOLDINGS INC |
| HUT | 669228291 | 0.0001 | 0.0001 | HUT 8 CORP |
| PL | 530906124 | 0.0001 | 0.0001 | PLANET LABS PBC |
| CIEN | 41045553 | 0.0001 | 0.0001 | CIENA CORP |
| NBIS | 88819736 | 0.0001 | 0.0001 | NEBIUS GROUP NV |
| RVMD | 403666731 | 0.0001 | 0.0001 | REVOLUTION MEDICINES INC |
| WULF | 532497563 | 0.0001 | 0.0001 | TERAWULF INC |

A SizeIncrement of 0.0001 signals fractional eligibility at the
instrument layer for every name. The whole-share-only permission-sync
escape of the stage prompt therefore does not apply: the instruments
are eligible, and what refused was the API channel.

## Task 2: decimal quantity, both names, verbatim

Quote snapshot MU: bid 903.0 ask 903.1 last 903.09 close 910.43 captured 2026-08-25T03:05:36.438723Z (delayed type 3, market closed).
Quote snapshot TE: bid 4.3 ask 4.35 last 4.35 close 4.32 captured 2026-08-25T03:05:56.813352Z (delayed type 3, market closed).
Quantity MU: 45.00 USD / 903.1 (delayed ask) = 0.0498.
Quantity TE: 45.00 USD / 4.35 (delayed ask) = 10.3448.

### decimal-mkt-MU

    03:05:36.451161 status=PendingSubmit
    03:05:36.713316 status=Cancelled Error 10243, reqId 25: Fractional-sized order cannot be placed via API. Please use desktop version to place this order.
    terminal status: Cancelled, filled 0.0

### decimal-lmt-MU

    03:05:44.472366 status=PendingSubmit
    03:05:44.813374 status=Cancelled Error 10243, reqId 26: Fractional-sized order cannot be placed via API. Please use desktop version to place this order.
    terminal status: Cancelled, filled 0.0

### decimal-mkt-TE

    03:05:56.817169 status=PendingSubmit
    03:05:57.043623 status=Cancelled Error 10243, reqId 29: Fractional-sized order cannot be placed via API. Please use desktop version to place this order.
    terminal status: Cancelled, filled 0.0

Every decimal order was refused at validation with error 10243:
"Fractional-sized order cannot be placed via API. Please use desktop
version to place this order." The refusal is immediate and
independent of market hours, order type, and outsideRth.

## Task 3: cashQty, the contradicted path, verbatim

    03:06:04.837953 status=PendingSubmit
    03:06:05.105175 status=Cancelled Error 10244, reqId 30: Cash Quantity cannot be used for this order
    terminal status: Cancelled, filled 0.0

Error 10244: "Cash Quantity cannot be used for this order." The June
2026 IBKR staff claim is confirmed by behaviour and the March 2026
third-party claim is refuted: cashQty is refused for US stock orders
on this channel, with no silent rounding, because nothing was
accepted to round.

## The whole-share control

    03:07:06.150879 status=PendingSubmit
    03:07:06.796010 status=ValidationError Warning 399, reqId 3: Order Message: BUY 1 TE NYSE Warning: Your order will not be placed at the exchange until 2026-08-25 09:30:00 US/Eastern.
    03:07:06.836362 status=PreSubmitted
    then cancelled before the open, filled 0.0

One whole share of TE was ACCEPTED and queued for the 09:30 ET open,
then cancelled. The channel works, Read-Only is off, and the
fractional refusals are specific to fractional sizing.

## Task 4: commissions

No order filled, so no commission was observed. Nothing exists to
label INDICATIVE-ONLY and nothing migrates into the cost model.
Billing regimes remain registered as settled only by D.1's live
statement reconciliation, which BLOCKED now makes moot at this stake.

## Task 5: flat, and the verdict

Positions on [paper account ID removed] at 2026-08-25T03:06:14.850255Z: [] 
Positions on [paper account ID removed] at 2026-08-25T03:07:17.172526Z: [] 

Section 0 fires BLOCKED. The registered GO bar requires the API to
accept fractional quantities at 45 USD per name. The API refused
fractional quantities however phrased: decimal totalQuantity by
market order, decimal totalQuantity by limit order, decimal on a
second name, and cashQty, each with an explicit error, while a
whole-share control was accepted. Per Section 0, phases C and D
stop. Per Section 6, DEGRADED whole-share sizing stays closed at
this stake. Phase B proceeds unchanged: the shadow series needs no
broker and the signal question still gets answered. Per ADR-003, an
Alpaca Canadian launch would reopen the table.

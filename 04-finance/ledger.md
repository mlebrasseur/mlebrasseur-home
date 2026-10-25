# Ledger

Last updated: 2026-10-25

This is the source of truth for personal money movement. User-reported payments are identified below; receipt of a payment by its recipient is distinguished from submission.

| Date | Amount | Currency | Paid To / From | Category | Method | Related Project | Source | Notes |
|---|---:|---|---|---|---|---|---|---|
| 2026-06-06 | -600.00 | CAD | Steve Charbonneau | Inspection | Interac transfer | Inspection | SRC-2026-015, SRC-2026-061 | Deposited; reference CACN9PX2; agreement also acknowledges receipt. Same payment, not two expenses. |
| 2026-08-10 | -130038.27 | CAD | LRV Notaires trust account | Closing funds | Assyst Paiement (inferred) | Legal closing | SRC-2026-043, SRC-2026-045, SRC-2026-059 | Submission date user-reported; amount and receipt now supported by buyer trust statement. Exact receipt date and Assyst method not independently established by statement. |
| 2026-08-26 | -655.62 | CAD | LRV Notaires | Closing settlement / fee balance | Interac debit | Legal closing | SRC-2026-056, SRC-2026-059, SRC-2026-060 | Approved debit receipt attached to paid invoice. Trust allocates 1,382.65 to fees and 655.62 to net seller adjustment; this additional debit reconciles full 2,038.27 fee. Do not duplicate as another adjustment payment. |
| 2026-09-01 | -2590.74 | CAD | Caisse Desjardins du Centre et de l'Est de Laval | Mortgage | Not separately confirmed | Mortgage | SRC-2026-057, SRC-2026-063 | First payment made September 1, user-reported September 8. Principal/interest split and banking evidence not supplied. |
| 2026-09-08 | -186.52 | CAD | Centre de services scolaire des Affluents | School tax | Online bill payment (context-inferred) | Taxes | SRC-2026-058, SRC-2026-062 | User reported payment made now; September 10 installment. Reference 00437000000596090119; confirmation number and recipient posting unconfirmed. |
| Exact date unspecified; “during the week” | -4650.00 | CAD | Painting contractor (name unspecified) | Renovation — painting | Unspecified | General renovations | SRC-2026-065, SRC-2026-078 | Paid in full, homeowner-reported October 25; 0 CAD remaining. Work completed by move day (recorded September 27). Week boundaries and tax breakdown unspecified; aggregate payment record, individual transactions not supplied. |

## Closing Allocation (Not Additional Personal Transactions)

SRC-2026-059 records 130,038.27 CAD buyer funds plus 512,000.00 CAD mortgage proceeds received by LRV. Uses are 640,655.62 CAD payable to seller and 1,382.65 CAD toward notary fees, with zero buyer balance/refund. Mortgage proceeds and trust allocations are not counted again as personal spending.

Total personal closing cash is 130,693.89 CAD (130,038.27 + 655.62): down payment 128,000.00 + paid notary invoice 2,038.27 + net closing adjustment 655.62. Occupancy and school-tax credits are netted in that adjustment, not separate cash receipts. (SRC-2026-056, SRC-2026-059, SRC-2026-060)

Painting completion/payment source: [SRC-2026-078](../01-sources/chat/2026/2026-10-25-property-stains-and-attic-check.md).

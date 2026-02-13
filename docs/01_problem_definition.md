# Problem Definition

Classic P&L reporting for subscription products often counts **all observed behavior** of subscribers as "caused by subscription".
For a subscription like Plus, adoption changes customer behavior; therefore the correct view is **uplift P&L**:

- What additional orders/items/NMV/profit happened **because Plus existed**?
- How much subscription revenue should be allocated to the month based on active days?

This repository implements a daily uplift method by RFM segment, and then aggregates to a monthly uplift P&L.

# Diagram Demonstration

---

## mermaid

```mermaid
flowchart TD

Start([開始])
Order[注文受付]
Check{在庫あり?}
Ship[出荷処理]
Wait[入荷待ち]
End([終了])

Start --> Order
Order --> Check

Check -->|Yes| Ship
Check -->|No| Wait

Ship --> End
Wait --> End
```

---

## PlantUML

```plantuml
@startuml test

start

:注文受付;

if (在庫あり?) then (Yes)
  :出荷処理;
  :発送通知;
else (No)
  :入荷待ち;
  :顧客へ連絡;
endif

stop

@enduml
```

---

## Graphviz

```dot
digraph OrderFlow {
    rankdir=TB;

    Start [shape=ellipse];
    Order [shape=box, label="注文受付"];
    Stock [shape=diamond, label="在庫あり?"];
    Ship [shape=box, label="出荷処理"];
    Wait [shape=box, label="入荷待ち"];
    End [shape=ellipse];

    Start -> Order;
    Order -> Stock;

    Stock -> Ship [label="Yes"];
    Stock -> Wait [label="No"];

    Ship -> End;
    Wait -> End;
}
```

---

## D2

```d2
start: 開始
order: 注文受付
stock: 在庫あり？
ship: 出荷処理
wait: 入荷待ち
end: 終了

start -> order
order -> stock

stock -> ship: Yes
stock -> wait: No

ship -> end
wait -> end

stock.shape: diamond
```

---

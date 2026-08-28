# mermaid Demonstration

---

## フローチャート

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

## シーケンス図

```mermaid
sequenceDiagram

actor User
participant Web
participant API
participant DB

User->>Web: 注文
Web->>API: POST /orders
API->>DB: INSERT

DB-->>API: OK
API-->>Web: 201 Created

Web-->>User: 注文完了
```

---

## クラス図

```mermaid
classDiagram

class Customer {
    +int id
    +string name
    +placeOrder()
}

class Order {
    +int orderId
    +ship()
}

Customer --> Order
```

---

## 状態遷移図

```mermaid
stateDiagram-v2

[*] -->*Draft

Draft --> Review
Review --> Approved
Review --> Rejected

Rejected --> Draft

Approved --> [*]
```

---

## ER図

```mermaid
erDiagram

CUSTOMER ||--o{ ORDER : places

CUSTOMER {
    int id
    string name
    string email
}

ORDER {
    int id
    date order_date
}
```

---

## ユースケース図風

```mermaid
flowchart LR

Customer([顧客])

UC1([商品検索])
UC2([注文])
UC3([決済])

Customer --> UC1
Customer --> UC2
Customer --> UC3
```

---

## システム構成図

```mermaid
flowchart LR

User[利用者]
Web[Web App]
API[API Server]
DB[(MySQL)]

User --> Web
Web --> API
API --> DB
```

---

## AWS風アーキテクチャ図

```mermaid
flowchart TB

User[User]

subgraph AWS
  ALB[Load Balancer]

  subgraph ECS
    Web1[Web1]
    Web2[Web2]
  end

  RDS[(RDS)]
end

User --> ALB

ALB --> Web1
ALB --> Web2

Web1 --> RDS
Web2 --> RDS
```

---

## ガントチャート

```mermaid
gantt
    title 開発スケジュール
    dateFormat YYYY-MM-DD

    section 設計
    要件定義 :done, a1, 2026-07-01, 5d
    基本設計 :active, a2, 2026-07-06, 7d

    section 実装
    コーディング :a3, 2026-07-13, 10d
```

---

## 円グラフ

```mermaid
pie title 売上構成比
    "製品A" : 45
    "製品B" : 30
    "製品C" : 25
```

---

## Gitフロー

```mermaid
gitGraph
   commit
   branch feature
   checkout feature
   commit
   commit
   checkout main
   merge feature
```

---

## 総合デモ（おすすめ）

```mermaid
flowchart LR

Customer[顧客]
Browser[Browser]
API[API Server]
DB[(Database)]

Customer --> Browser
Browser -->|POST /orders| API
API -->|INSERT| DB
DB -->|OK| API
API -->|201 Created| Browser
Browser --> Customer
```

---

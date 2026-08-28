# PlantUML Demonstration

---

## アクティビティ図（業務フロー）

```plantuml
@startuml

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

## シーケンス図

```plantuml
@startuml

actor User
participant Web
participant API
database DB

User -> Web : 注文
Web -> API : POST /orders
API -> DB : INSERT Order

DB --> API : OK
API --> Web : 201 Created
Web --> User : 注文完了

@enduml
```

---

## クラス図

```plantuml
@startuml

class Customer {
  +id : int
  +name : String
  +placeOrder()
}

class Order {
  +orderId : int
  +ship()
}

Customer "1" --> "*" Order

@enduml
```

---

## ER図

```plantuml
@startuml

entity Customer {
  id : bigint <<PK>>
  name : varchar
  email : varchar
}

entity Order {
  id : bigint <<PK>>
  order_date : datetime
}

Customer ||--o{ Order

@enduml
```

---

## 状態遷移図

```plantuml
@startuml

[*] --> Draft

Draft --> Review
Review --> Approved
Review --> Rejected

Rejected --> Draft

Approved --> [*]

@enduml
```

---

## ユースケース図

```plantuml
@startuml

left to right direction

actor Customer as "顧客"

rectangle "ECサイト" {

  usecase "商品検索" as UC1
  usecase "注文" as UC2
  usecase "決済" as UC3

  Customer --> UC1
  Customer --> UC2
  Customer --> UC3
}

@enduml
```

---

## コンポーネント図

```plantuml
@startuml

left to right direction

actor Customer as "顧客"

rectangle "ECサイト" {

  usecase "商品検索" as UC1
  usecase "注文" as UC2
  usecase "決済" as UC3

  Customer --> UC1
  Customer --> UC2
  Customer --> UC3
}

@enduml
```

---

## AWS風システム構成図

```plantuml
@startuml

node "Internet" {
    actor User
}

cloud "AWS" {

    node "ALB" {
        component LoadBalancer
    }

    node "ECS" {
        component Web1
        component Web2
    }

    database RDS
}

User --> LoadBalancer

LoadBalancer --> Web1
LoadBalancer --> Web2

Web1 --> RDS
Web2 --> RDS

@enduml
```

---

## Ganttチャート

```plantuml
@startgantt

Project starts 2026-08-01

[要件定義] lasts 5 days
[基本設計] lasts 7 days
[実装] lasts 14 days
[テスト] lasts 5 days

[基本設計] starts at [要件定義]'s end
[実装] starts at [基本設計]'s end
[テスト] starts at [実装]'s end

@endgantt
```

---

## 総合デモ（おすすめ）

```plantuml
@startuml

actor User
participant Web
participant API
database DB

User -> Web : 注文
Web -> API : POST /orders

activate API

API -> DB : INSERT

DB --> API : OK

API --> Web : 201 Created
Web --> User : 注文完了

deactivate API

@enduml

```

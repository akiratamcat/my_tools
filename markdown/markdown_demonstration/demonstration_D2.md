# D2 Demonstration

---

## 基本フロー

```d2
start: 開始
order: 注文受付
check: 在庫確認
ship: 出荷
end: 終了

start -> order
order -> check
check -> ship
ship -> end
```

---

## 条件分岐

```d2
注文受付 -> 在庫確認

在庫確認 -> 出荷: Yes
在庫確認 -> 入荷待ち: No

出荷 -> 終了
入荷待ち -> 終了

在庫確認.shape: diamond
```

---

## システム構成図

```d2
User -> WebApp
WebApp -> APIServer
APIServer -> Database

User.shape: person
Database.shape: cylinder
```

---

## AWS風アーキテクチャ図

```d2
ユーザー -> ALB

ALB -> Web1
ALB -> Web2

Web1 -> RDS
Web2 -> RDS

RDS.shape: cylinder

Web1.style.fill: "#d5e8d4"
Web2.style.fill: "#d5e8d4"
ALB.style.fill: "#dae8fc"
RDS.style.fill: "#ffe6cc"
```

---

## 階層構造

```d2
ECサイト: {
  Frontend: {
    WebApp
  }

  Backend: {
    APIServer
    Batch
  }

  Database
}

WebApp -> APIServer
APIServer -> Database
Batch -> Database
```

---

## クラス図風

```d2
Customer: {
  shape: class

  id: int
  name: string

  placeOrder()
}

Order: {
  shape: class

  id: int
  orderDate: date

  ship()
}

Customer -> Order
```

---

## 状態遷移図

```d2
Draft -> Review
Review -> Approved
Review -> Rejected
Rejected -> Draft
```

---

## デモ向け総合サンプル（おすすめ）

```d2
direction: right

Customer.shape: person
Database.shape: cylinder

Customer -> Browser: 注文

Browser -> APIServer: POST /orders

APIServer -> Database: INSERT

Database -> APIServer: OK

APIServer -> Browser: 201 Created

Browser -> Customer: 注文完了

Browser.style.fill: "#dae8fc"
APIServer.style.fill: "#d5e8d4"
Database.style.fill: "#ffe6cc"
```

---

# PayPal 支付按钮代码

## 套餐配置

### Starter Guide - $30
```html
<!-- PayPal Button for Starter Guide ($30) -->
<div id="paypal-button-starter"></div>
<script src="https://www.paypal.com/sdk/js?client-id=YOUR_CLIENT_ID&currency=USD"></script>
<script>
  paypal.Buttons({
    createOrder: function(data, actions) {
      return actions.order.create({
        purchase_units: [{
          amount: {
            value: '30.00',
            currency_code: 'USD'
          },
          description: 'Starter Guide - Complete hospital database and treatment guides'
        }]
      });
    },
    onApprove: function(data, actions) {
      return actions.order.capture().then(function(details) {
        alert('Thank you ' + details.payer.name.given_name + '! Your Starter Guide will be sent to your email within 24 hours.');
        // TODO: Send confirmation email and deliver digital product
      });
    }
  }).render('#paypal-button-starter');
</script>
```

### Standard Package - $299
```html
<!-- PayPal Button for Standard Package ($299) -->
<div id="paypal-button-standard"></div>
<script>
  paypal.Buttons({
    createOrder: function(data, actions) {
      return actions.order.create({
        purchase_units: [{
          amount: {
            value: '299.00',
            currency_code: 'USD'
          },
          description: 'Standard Package - Hospital booking and medical record translation'
        }]
      });
    },
    onApprove: function(data, actions) {
      return actions.order.capture().then(function(details) {
        alert('Thank you ' + details.payer.name.given_name + '! Our team will contact you within 24 hours to start your medical journey.');
        // TODO: Send confirmation email and assign case manager
      });
    }
  }).render('#paypal-button-standard');
</script>
```

### Premium Package - $899
```html
<!-- PayPal Button for Premium Package ($899) -->
<div id="paypal-button-premium"></div>
<script>
  paypal.Buttons({
    createOrder: function(data, actions) {
      return actions.order.create({
        purchase_units: [{
          amount: {
            value: '899.00',
            currency_code: 'USD'
          },
          description: 'Premium Package - Full concierge services with on-site support'
        }]
      });
    },
    onApprove: function(data, actions) {
      return actions.order.capture().then(function(details) {
        alert('Thank you ' + details.payer.name.given_name + '! Your dedicated concierge will contact you within 12 hours.');
        // TODO: Send confirmation email and assign concierge
      });
    }
  }).render('#paypal-button-premium');
</script>
```

---

## 完整定价页面代码

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Pricing - China Hospitals Guide</title>
    <script src="https://www.paypal.com/sdk/js?client-id=YOUR_CLIENT_ID&currency=USD"></script>
    <style>
        .pricing-container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 2rem;
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 2rem;
        }
        
        .pricing-card {
            border: 2px solid #e0e0e0;
            border-radius: 12px;
            padding: 2rem;
            text-align: center;
            transition: transform 0.3s, box-shadow 0.3s;
        }
        
        .pricing-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        }
        
        .pricing-card.featured {
            border-color: #1e3c72;
            background: linear-gradient(135deg, #f8f9fa 0%, #e3f2fd 100%);
        }
        
        .pricing-card h3 {
            font-size: 1.5rem;
            color: #1e3c72;
            margin-bottom: 0.5rem;
        }
        
        .price {
            font-size: 3rem;
            font-weight: bold;
            color: #1e3c72;
            margin: 1rem 0;
        }
        
        .price span {
            font-size: 1rem;
            color: #666;
        }
        
        .features {
            list-style: none;
            padding: 0;
            margin: 2rem 0;
            text-align: left;
        }
        
        .features li {
            padding: 0.5rem 0;
            border-bottom: 1px solid #eee;
        }
        
        .features li:before {
            content: "✓ ";
            color: #4caf50;
            font-weight: bold;
        }
        
        .paypal-button-container {
            margin-top: 1.5rem;
        }
    </style>
</head>
<body>
    <div class="pricing-container">
        <!-- Starter Guide -->
        <div class="pricing-card">
            <h3>Starter Guide</h3>
            <div class="price">$30<span>USD</span></div>
            <p>Perfect for independent travelers</p>
            <ul class="features">
                <li>Complete hospital database (40+ hospitals)</li>
                <li>Treatment cost guides by specialty</li>
                <li>Visa application guidance</li>
                <li>City guides (Beijing, Shanghai, Guangzhou)</li>
                <li>Email support</li>
            </ul>
            <div id="paypal-button-starter" class="paypal-button-container"></div>
        </div>
        
        <!-- Standard Package -->
        <div class="pricing-card featured">
            <h3>Standard Package</h3>
            <div class="price">$299<span>USD</span></div>
            <p>Most popular choice</p>
            <ul class="features">
                <li>Everything in Starter Guide</li>
                <li>Hospital appointment booking</li>
                <li>Medical record translation</li>
                <li>Pre-arrival coordination</li>
                <li>Invitation letter for visa</li>
                <li>Dedicated case manager</li>
                <li>Priority email support</li>
            </ul>
            <div id="paypal-button-standard" class="paypal-button-container"></div>
        </div>
        
        <!-- Premium Package -->
        <div class="pricing-card">
            <h3>Premium Package</h3>
            <div class="price">$899<span>USD</span></div>
            <p>Full concierge experience</p>
            <ul class="features">
                <li>Everything in Standard Package</li>
                <li>Airport pickup and drop-off</li>
                <li>On-site assistance (5 days)</li>
                <li>Accommodation booking assistance</li>
                <li>Translation services during treatment</li>
                <li>Post-treatment follow-up</li>
                <li>24/7 dedicated concierge</li>
            </ul>
            <div id="paypal-button-premium" class="paypal-button-container"></div>
        </div>
    </div>
    
    <script>
        // Initialize PayPal buttons
        paypal.Buttons({
            createOrder: function(data, actions) {
                return actions.order.create({
                    purchase_units: [{
                        amount: { value: '30.00', currency_code: 'USD' },
                        description: 'Starter Guide'
                    }]
                });
            },
            onApprove: function(data, actions) {
                return actions.order.capture().then(function(details) {
                    window.location.href = '/thank-you.html?package=starter';
                });
            }
        }).render('#paypal-button-starter');
        
        paypal.Buttons({
            createOrder: function(data, actions) {
                return actions.order.create({
                    purchase_units: [{
                        amount: { value: '299.00', currency_code: 'USD' },
                        description: 'Standard Package'
                    }]
                });
            },
            onApprove: function(data, actions) {
                return actions.order.capture().then(function(details) {
                    window.location.href = '/thank-you.html?package=standard';
                });
            }
        }).render('#paypal-button-standard');
        
        paypal.Buttons({
            createOrder: function(data, actions) {
                return actions.order.create({
                    purchase_units: [{
                        amount: { value: '899.00', currency_code: 'USD' },
                        description: 'Premium Package'
                    }]
                });
            },
            onApprove: function(data, actions) {
                return actions.order.capture().then(function(details) {
                    window.location.href = '/thank-you.html?package=premium';
                });
            }
        }).render('#paypal-button-premium');
    </script>
</body>
</html>
```

---

## 配置说明

### 1. 获取 PayPal Client ID
1. 登录 PayPal Developer Dashboard: https://developer.paypal.com/
2. 创建 App（Live 环境）
3. 复制 Client ID
4. 替换代码中的 `YOUR_CLIENT_ID`

### 2. 支付完成后处理
需要设置 webhook 或服务器端处理：
- 发送确认邮件
- 交付数字产品（Starter Guide）
- 分配客户经理（Standard/Premium）
- 更新订单数据库

### 3. 测试
使用 PayPal Sandbox 环境测试：
- 创建 Sandbox 账户
- 使用测试信用卡
- 验证支付流程

---

*最后更新: 2026-03-05*

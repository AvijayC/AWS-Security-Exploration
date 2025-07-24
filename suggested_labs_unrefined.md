# AWS Security Specialty – Comprehensive Lab Catalogue

_A 25-lab, hands-on system to deeply internalize AWS Security Specialty exam concepts. Prioritized by exam coverage and hands-on clarity._

---

## 🔥 Legend

- Labs marked **🔥** directly target **missed questions** from your recent practice exam.
- Labs are ordered **by impact and urgency**—not domain.

---

## 1. Identity & Access / KMS

### Lab 1 🔥 – KMS Multipart Upload Troubleshooting
- Reproduce an `AccessDenied` error during multipart uploads with SSE-KMS.
- Add the required `kms:GenerateDataKey*` and `kms:Decrypt` permissions to:
  - S3 bucket policy
  - CMK key policy
- Confirm success via CLI upload of file >5GB.

### Lab 2 🔥 – 24-Hour Key Retirement Myth-Busting
- Attempt to schedule key deletion with a 1-day window (should fail).
- Verify 7-day is the minimum deletion window.
- Disable a key, test permissions, then re-enable to restore functionality.

### Lab 3 – Envelope Encryption (Manual)
- Generate a DEK using `GenerateDataKey`.
- Encrypt plaintext locally using the DEK.
- Delete the DEK.
- Re-decrypt using the ciphertext DEK and CMK.

### Lab 4 🔥 – Cross-Account S3 Read/Write
- Use IAM role trust policy + S3 bucket policy scoped to `aws:PrincipalOrgID`.
- Grant Account A read-write and Account B read-only access to a bucket.

---

## 2. Networking / Infrastructure

### Lab 5 🔥 – Interface VPC Endpoint to Private API Gateway (Same Account)
- Build a private API Gateway.
- Create VPC endpoint with restrictive policy allowing only specific API ARNs.
- Test DNS resolution and functionality from within the VPC.

### Lab 6 🔥 – Cross-Account Private API Gateway via Interface Endpoint
- Repeat Lab 5, but requester and acceptor in different accounts.
- Verify VPC endpoint policy, DNS, and access rights.

### Lab 7 🔥 – VPC Peering + SG Referencing Across Regions
- Peer VPC1 and VPC2.
- In VPC1 SG, reference a SG from VPC2 in a rule.
- Verify communication across VPCs via peering and SG logic.

### Lab 8 🔥 – PrivateLink Troubleshooting
- Create an NLB-backed PrivateLink service.
- Intentionally misconfigure:
  - SG egress rules
  - Subnet routes
- Use CloudWatch metrics to diagnose and fix.

### Lab 9 – Central Inspection VPC with Flow Logs + Traffic Mirroring
- Build hub VPC with traffic mirroring enabled.
- Use flow logs to capture access violations.
- Test VPC-to-VPC packet flow inspection.

---

## 3. Data Protection (Edge Services)

### Lab 10 🔥 – CloudFront + Authorization Header Forwarding
- Setup CloudFront distribution to forward the `Authorization` header.
- Configure origin request policy properly.
- Test signed vs. open URLs and their results.

### Lab 11 – TLS 1.0 Legacy Client Support
- Create a CloudFront distribution using a legacy security policy.
- Use ACM with RSA-2048 cert.
- Verify backward compatibility with TLS 1.0 clients.

### Lab 12 🔥 – ALB with Mutual TLS (mTLS)
- Import a client certificate into ACM.
- Configure ALB listener for mTLS handshake.
- Verify bidirectional TLS handshake using `openssl` or test client.

---

## 4. Monitoring / Incident Response

### Lab 13 🔥 – GuardDuty → Auto-Isolation via Lambda
- Enable GuardDuty with test findings.
- Create EventBridge rule matching `BruteForce/RDP`.
- Trigger Lambda to apply a quarantine SG or stop instance.

### Lab 14 🔥 – Security Hub Full Stack Integration
- Enable Security Hub and integrate:
  - GuardDuty
  - AWS Config
  - Inspector
- Configure severity-based finding suppression.
- Route high-severity alerts to Slack/SNS.

### Lab 15 🔥 – S3 PutObjectAcl Detection
- Enable CloudTrail data events on S3.
- Create EventBridge rule to detect `PutObjectAcl` usage.
- Push alerts to SNS/email.

### Lab 16 – ACM Cert Expiry Alerting
- Use Config managed rule `acm-certificate-expiration-check`.
- Setup EventBridge alert at 30-day window.
- Fan-out to Slack/SNS or email.

### Lab 17 🔥 – Root User Activity Alarm
- Build CloudTrail trail capturing console logins.
- Filter on `userIdentity.type = "Root"`.
- Metric filter + CloudWatch alarm → SNS alert.

---

## 5. Messaging & Email Security

### Lab 18 🔥 – SES TLS-Only API Calls
- Setup VPC endpoint for SES.
- Block port 80 outbound (HTTP) to enforce TLS.
- Use SigV4 signed API requests only.

### Lab 19 – IAM Policy for SES Sending Identity
- Write IAM policy scoping `ses:SendEmail` to specific verified identity (email or domain).
- Test policy enforcement using SDK or CLI.

---

## 6. Deployment & Governance

### Lab 20 🔥 – Secrets Manager Rotation in Private Subnet
- Put Lambda in private subnet with no Internet.
- Add Secrets Manager VPC endpoint.
- Rotate RDS credentials using Lambda function.

### Lab 21 🔥 – CloudFormation Guarded Template
- Write CloudFormation Guard rules:
  - Block unencrypted EBS
  - Deny 0.0.0.0/0 SGs
  - Enforce EC2 instance types
- Use `cfn-guard` CLI to validate templates.

### Lab 22 🔥 – SCP to Restrict Region
- Apply Service Control Policy denying `ec2:RunInstances` if region ≠ `us-west-2`.
- Test policy in management account.

### Lab 23 – Permission Boundary Sandboxing
- Use IAM permission boundaries to constrain developers to:
  - Only launch t3.micro
  - Only use nonprod-* prefixes
- Demonstrate effects in CI/CD context.

### Lab 24 🔥 – Auto-Revoke Public IAM Keys
- Simulate public GitHub AccessKey finding.
- EventBridge rule auto-disables IAM key.
- Sends notification to PagerDuty or SNS.

---

## 7. WAF & Front-Door Defense

### Lab 25 🔥 – WAF Brute-Force Login Mitigation
- Create WAFv2 rule on path `/login`:
  - Rate-limit by IP
  - CAPTCHA or challenge rule
- Push matched counts to CloudWatch metrics.
- Simulate attack and confirm mitigation.

---

## Total Lab Count: **25**

Estimated time to complete (hands-on + notes): **50–60 hours**.

---

## Suggested Tracking Columns (For Google Sheets or Notion)

| Lab # | Title | Status | Notes | Date Started | Date Completed | Key Lessons | Related Exam Domain |
|-------|-------|--------|-------|--------------|----------------|-------------|----------------------|

---

## Tip

You are not doing these to "feel productive." You're doing them to:
- Build **hands-on muscle memory**
- Surface your **misconceptions**
- Create **proof-of-work artifacts**
- Reduce test anxiety through repetition

When in doubt, break and fix everything.

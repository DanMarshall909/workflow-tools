# Universal Test Naming Principles

## The Golden Rule
**Name tests as if explaining the scenario to a business stakeholder who doesn't know the code.**

## Core Philosophy

Tests are not just code verification tools - they are living documentation of your system's behavior. A well-named test tells a story about what your application does and why it matters to users.

## Universal Principles (Any Language)

### 1. Focus on Business Behavior, Not Implementation
```
❌ BAD:  test_should_return_true_when_valid
✅ GOOD: test_user_can_access_their_own_data

❌ BAD:  test_database_insert_works
✅ GOOD: test_new_account_persists_after_creation

❌ BAD:  test_null_check_throws_exception  
✅ GOOD: test_missing_required_fields_prevent_submission
```

### 2. Remove Technical Jargon
- No method names
- No class names (unless they represent domain concepts)
- No technical implementation details
- No database/API/framework specifics

### 3. Use Natural Language
- Write complete thoughts
- Use underscores or spaces (language-dependent) for readability
- Avoid abbreviations
- Write in active voice

### 4. The "Should" Ban
"Should" describes intention, not behavior. Tests verify what IS, not what SHOULD BE.

```
❌ BAD:  should_calculate_tax_correctly
✅ GOOD: calculates_sales_tax_for_online_purchases

❌ BAD:  should_send_email_on_registration
✅ GOOD: new_users_receive_welcome_email
```

## Test Naming Patterns by Scenario

### User Actions
```
Pattern: [user/actor] [action] [outcome/behavior]

Examples:
- user_can_reset_forgotten_password
- admin_sees_all_pending_approvals
- guest_cannot_access_private_content
- customer_receives_order_confirmation
```

### Business Rules
```
Pattern: [condition/context] [rule/behavior]

Examples:
- expired_coupons_are_rejected_at_checkout
- orders_over_100_dollars_ship_free
- inactive_accounts_require_reactivation
- passwords_must_contain_special_characters
```

### System Behaviors
```
Pattern: [system/component] [behavior] [condition]

Examples:
- search_returns_relevant_results_first
- notifications_arrive_within_five_seconds
- reports_generate_in_pdf_format
- backups_run_every_night_at_midnight
```

### Error Scenarios
```
Pattern: [error condition] [user experience]

Examples:
- network_failure_shows_retry_option
- invalid_input_displays_helpful_message
- timeout_preserves_user_data
- system_overload_queues_requests_gracefully
```

## Organizing Test Suites

### By User Journey
```
UserRegistration/
├── new_user_can_create_account
├── email_verification_activates_account
├── duplicate_email_prevents_registration
└── weak_password_shows_requirements
```

### By Business Feature
```
ShoppingCart/
├── items_persist_between_sessions
├── quantity_changes_update_total_price
├── out_of_stock_items_show_unavailable
└── discounts_apply_before_tax_calculation
```

### By System Capability
```
DataExport/
├── users_can_download_their_data
├── export_excludes_private_fields
├── large_exports_send_download_link
└── exports_comply_with_gdpr_format
```

## Anti-Patterns to Avoid

### 1. Testing Implementation Details
```
❌ BAD:  mock_repository_returns_user_object
✅ GOOD: existing_users_can_sign_in

❌ BAD:  spy_called_with_correct_parameters
✅ GOOD: email_sent_to_correct_recipient
```

### 2. Vague or Generic Names
```
❌ BAD:  test_happy_path
✅ GOOD: valid_credit_card_completes_purchase

❌ BAD:  test_edge_case
✅ GOOD: order_with_zero_items_cannot_checkout
```

### 3. Technical Stack References
```
❌ BAD:  redis_cache_stores_session_data
✅ GOOD: user_sessions_persist_across_visits

❌ BAD:  postgresql_transaction_rollback_works
✅ GOOD: failed_payments_do_not_charge_customer
```

## Documentation Through Tests

Good test names eliminate the need for comments:

```
// ❌ This test checks if the user can update their profile
// after email verification is complete
test_update_profile_after_verification()

// ✅ No comment needed
test_verified_users_can_update_profile_information()
```

## Cultural Considerations

### Domain Language
Use terminology familiar to your business domain:

**E-commerce:**
- customer_can_track_shipment
- abandoned_carts_send_reminder_email

**Healthcare:**
- patient_medical_history_requires_consent
- prescriptions_require_doctor_approval

**Finance:**
- transactions_appear_in_chronological_order
- overdraft_protection_prevents_negative_balance

## The Litmus Test

Ask yourself: **"If I showed this test name to a product manager, would they understand what it verifies?"**

If the answer is no, rewrite it.

## Quick Reference Card

| Concept | Bad Example | Good Example |
|---------|-------------|--------------|
| User Actions | `testLogin()` | `registered_user_can_sign_in` |
| Validation | `testValidation()` | `form_rejects_invalid_email_format` |
| Permissions | `testAuth()` | `only_owner_can_delete_account` |
| Business Rules | `testCalculation()` | `sales_tax_applies_to_digital_goods` |
| Error Handling | `test500Error()` | `server_error_shows_maintenance_page` |
| Performance | `testSpeed()` | `search_results_load_within_two_seconds` |
| Integration | `testAPICall()` | `weather_data_updates_hourly` |

## Remember

> "Tests are the only documentation that doesn't lie." - Unknown

Make your test names tell the truth about what your system does, in language everyone can understand.

## References
- [Enterprise Craftsmanship: You Naming Tests Wrong](https://enterprisecraftsmanship.com/posts/you-naming-tests-wrong/)
- [Growing Object-Oriented Software, Guided by Tests](http://www.growing-object-oriented-software.com/)
- [Test Driven Development: By Example](https://www.amazon.com/Test-Driven-Development-Kent-Beck/dp/0321146530)
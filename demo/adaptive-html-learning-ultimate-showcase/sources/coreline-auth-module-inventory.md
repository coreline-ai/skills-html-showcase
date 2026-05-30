# Coreline Auth module inventory

Generated from `src/coreline_auth` on 2026-05-30 for the landing brief factual source map.

## `src/coreline_auth/admin.py`

`CorelineAdminService`

## `src/coreline_auth/async_service.py`

`AsyncCorelineAuthService`

## `src/coreline_auth/authorization.py`

`PermissionDecision`, `AuthorizationContext`, `ResourceAuthorizer`

## `src/coreline_auth/csrf.py`

`CsrfToken`, `CsrfProtector`

## `src/coreline_auth/email.py`

`EmailSender`, `SentMagicLink`, `SentEmailVerification`, `SentPasswordReset`, `EmailTemplate`, `RenderedEmail`, `EmailTemplateSet`, `InMemoryEmailSender`, `SmtpEmailSender`

## `src/coreline_auth/encryption.py`

`SecretEnvelopeProtector`

## `src/coreline_auth/errors.py`

`CorelineAuthError`, `AuthConfigurationError`, `AuthValidationError`, `AuthenticationFailed`, `AuthorizationDenied`, `StorageError`

## `src/coreline_auth/fastapi_adapter.py`

`LoginRequest`, `MagicLinkRequest`, `MagicLinkConsumeRequest`, `EmailVerificationRequest`, `EmailVerificationConsumeRequest`, `PasswordResetRequest`, `PasswordResetConsumeRequest`, `request_context`, `token_from_request`, `mount_auth_routes`, `require_session`, `require_permission`, `AdminRoleRequest`, `AdminPasswordRequest`, `AdminReasonRequest`, `mount_admin_routes`

## `src/coreline_auth/fastapi_async_adapter.py`

`AsyncLoginRequest`, `AsyncMagicLinkRequest`, `AsyncMagicLinkConsumeRequest`, `mount_async_auth_routes`

## `src/coreline_auth/mfa.py`

`MfaSecretVault`, `InsecureMfaVaultWarning`, `InMemoryMfaSecretVault`, `generate_totp_secret`, `generate_recovery_code`, `totp_code`, `verify_totp_code`, `totp_counter_for_code`

## `src/coreline_auth/mfa_vault.py`

`SQLiteMfaSecretVault`, `RedisMfaSecretVault`

## `src/coreline_auth/models.py`

`now_utc`, `to_iso`, `from_iso`, `UserStatus`, `CredentialType`, `FlowType`, `AuthAssuranceLevel`, `MfaFactorType`, `AuthProfile`, `Role`, `AuthUser`, `AuthIdentity`, `AuthCredential`, `LoginFlow`, `AuthSession`, `AuthMfaFactor`, `AuthPasskeyChallenge`, `AuthRecoveryCode`, `AuditEvent`, `RequestContext`, `IssuedSession`, `MagicLinkChallenge`, `Principal`

## `src/coreline_auth/observability.py`

`MetricSink`, `InMemoryMetricSink`, `LoggingMetricSink`, `PrometheusTextMetricSink`, `JsonLineSecurityEventSink`

## `src/coreline_auth/ops_readiness.py`

`ReadinessStatus`, `ReadinessCheck`, `collect_readiness`, `assert_secret_safe`, `checks_to_json`, `checks_to_text`, `main`

## `src/coreline_auth/permissions.py`

`PermissionStatement`, `PolicyEngine`

## `src/coreline_auth/rate_limit.py`

`RateLimitDecision`, `RateLimiter`, `FixedWindowRateLimiter`

## `src/coreline_auth/redis_rate_limit.py`

`RedisFixedWindowRateLimiter`

## `src/coreline_auth/security.py`

`generate_token`, `hash_secret`, `compare_hash`, `hash_optional_context`, `normalize_email_address`, `hash_password`, `verify_password`, `verify_dummy_password`, `SafeReturnToPolicy`

## `src/coreline_auth/service.py`

`CorelineAuthConfig`, `CorelineAuthService`

## `src/coreline_auth/service_support.py`

`AuthServiceSupport`

## `src/coreline_auth/webauthn.py`

`VerifiedPasskeyRegistration`, `VerifiedPasskeyAssertion`, `generate_webauthn_challenge`, `verify_passkey_registration_response`, `verify_passkey_assertion_response`

## `src/coreline_auth/social/_utils.py`

`redact_token_response`

## `src/coreline_auth/social/connectors.py`

`OAuthConnector`, `GenericOIDCConnector`, `GoogleOAuthConnector`, `FacebookOAuthConnector`, `DevSocialConnector`

## `src/coreline_auth/social/discovery.py`

`OIDCMetadataClient`, `JWKSCache`, `discover_oidc_metadata`

## `src/coreline_auth/social/models.py`

`ProviderTokenVault`, `OAuthProviderConfig`, `OIDCProviderMetadata`, `OAuthPKCE`, `SocialProfile`, `OAuthStart`, `IdTokenClaims`

## `src/coreline_auth/social/verification.py`

`verify_google_id_token`, `verify_oidc_id_token`

## `src/coreline_auth/storage/async_base.py`

`AsyncAuthStorage`

## `src/coreline_auth/storage/async_memory.py`

`AsyncMemoryAuthStorage`

## `src/coreline_auth/storage/async_protocols.py`

`AsyncUserStore`, `AsyncIdentityStore`, `AsyncCredentialStore`, `AsyncLoginFlowStore`, `AsyncSessionStore`, `AsyncAuditEventStore`, `AsyncMfaFactorStore`, `AsyncRecoveryCodeStore`, `AsyncHealthCheckStore`

## `src/coreline_auth/storage/audit.py`

`AuditStorage`, `redact_audit_metadata`

## `src/coreline_auth/storage/base.py`

`AuthStorage`

## `src/coreline_auth/storage/memory.py`

`MemoryAuthStorage`

## `src/coreline_auth/storage/postgres.py`

`AsyncPostgresAuthStorage`

## `src/coreline_auth/storage/protocols.py`

`UserStore`, `IdentityStore`, `CredentialStore`, `LoginFlowStore`, `SessionStore`, `AuditEventStore`, `MfaFactorStore`, `RecoveryCodeStore`, `HealthCheckStore`

## `src/coreline_auth/storage/sqlalchemy_schema.py`

_No public top-level class/function discovered._

## `src/coreline_auth/storage/sqlite.py`

`SQLiteAuthStorage`

namespace Softozor.FusionAuth.TestDoubles;

using System;
using System.Collections.Generic;
using System.Diagnostics.CodeAnalysis;
using System.Threading.Tasks;
using io.fusionauth;
using io.fusionauth.domain;
using io.fusionauth.domain.api;
using io.fusionauth.domain.api.email;
using io.fusionauth.domain.api.identityProvider;
using io.fusionauth.domain.api.jwt;
using io.fusionauth.domain.api.passwordless;
using io.fusionauth.domain.api.report;
using io.fusionauth.domain.api.twoFactor;
using io.fusionauth.domain.api.user;
using io.fusionauth.domain.oauth2;
using io.fusionauth.domain.provider;

public class FusionAuthAsyncClient : IFusionAuthAsyncClient
{
    public const string SuccessChangePasswordId = "success-change-password-id";

    public Task<ClientResponse<ChangePasswordResponse>> ChangePasswordAsync(
        string changePasswordId,
        ChangePasswordRequest request)
    {
        if (changePasswordId == "success-change-password-id")
        {
            if (string.IsNullOrWhiteSpace(request.password))
            {
                return Task.FromResult(
                    new ClientResponse<ChangePasswordResponse>
                    {
                        statusCode = 400, exception = new Exception("malformed request")
                    });
            }

            var successResponse = new ClientResponse<ChangePasswordResponse>
            {
                statusCode = 200, successResponse = new ChangePasswordResponse()
            };
            return Task.FromResult(successResponse);
        }

        var failureResponse = new ClientResponse<ChangePasswordResponse>
        {
            statusCode = 404, exception = new Exception("could not find user from change password id")
        };
        return Task.FromResult(failureResponse);
    }

    public Task<ClientResponse<ActionResponse>> ActionUserAsync(ActionRequest request)
    {
        throw new NotImplementedException();
    }

    public Task<ClientResponse<RESTVoid>> ActivateReactorAsync(ReactorRequest request)
    {
        throw new NotImplementedException();
    }

    public Task<ClientResponse<FamilyResponse>> AddUserToFamilyAsync(Guid? familyId, FamilyRequest request)
    {
        throw new NotImplementedException();
    }

    public Task<ClientResponse<ActionResponse>> CancelActionAsync(Guid? actionId, ActionRequest request)
    {
        throw new NotImplementedException();
    }

    public Task<ClientResponse<RESTVoid>> ChangePasswordByIdentityAsync(ChangePasswordRequest request)
    {
        throw new NotImplementedException();
    }

    public Task<ClientResponse<RESTVoid>> CommentOnUserAsync(UserCommentRequest request)
    {
        throw new NotImplementedException();
    }

    public Task<ClientResponse<APIKeyResponse>> CreateAPIKeyAsync(Guid? keyId, APIKeyRequest request)
    {
        throw new NotImplementedException();
    }

    public Task<ClientResponse<ApplicationResponse>> CreateApplicationAsync(
        Guid? applicationId,
        ApplicationRequest request)
    {
        throw new NotImplementedException();
    }

    public Task<ClientResponse<ApplicationResponse>> CreateApplicationRoleAsync(
        Guid? applicationId,
        Guid? roleId,
        ApplicationRequest request)
    {
        throw new NotImplementedException();
    }

    public Task<ClientResponse<AuditLogResponse>> CreateAuditLogAsync(AuditLogRequest request)
    {
        throw new NotImplementedException();
    }

    public Task<ClientResponse<ConnectorResponse>> CreateConnectorAsync(Guid? connectorId, ConnectorRequest request)
    {
        throw new NotImplementedException();
    }

    public Task<ClientResponse<ConsentResponse>> CreateConsentAsync(Guid? consentId, ConsentRequest request)
    {
        throw new NotImplementedException();
    }

    public Task<ClientResponse<EmailTemplateResponse>> CreateEmailTemplateAsync(
        Guid? emailTemplateId,
        EmailTemplateRequest request)
    {
        throw new NotImplementedException();
    }

    public Task<ClientResponse<EntityResponse>> CreateEntityAsync(Guid? entityId, EntityRequest request)
    {
        throw new NotImplementedException();
    }

    public Task<ClientResponse<EntityTypeResponse>> CreateEntityTypeAsync(Guid? entityTypeId, EntityTypeRequest request)
    {
        throw new NotImplementedException();
    }

    public Task<ClientResponse<EntityTypeResponse>> CreateEntityTypePermissionAsync(
        Guid? entityTypeId,
        Guid? permissionId,
        EntityTypeRequest request)
    {
        throw new NotImplementedException();
    }

    public Task<ClientResponse<FamilyResponse>> CreateFamilyAsync(Guid? familyId, FamilyRequest request)
    {
        throw new NotImplementedException();
    }

    public Task<ClientResponse<FormResponse>> CreateFormAsync(Guid? formId, FormRequest request)
    {
        throw new NotImplementedException();
    }

    public Task<ClientResponse<FormFieldResponse>> CreateFormFieldAsync(Guid? fieldId, FormFieldRequest request)
    {
        throw new NotImplementedException();
    }

    public Task<ClientResponse<GroupResponse>> CreateGroupAsync(Guid? groupId, GroupRequest request)
    {
        throw new NotImplementedException();
    }

    public Task<ClientResponse<MemberResponse>> CreateGroupMembersAsync(MemberRequest request)
    {
        throw new NotImplementedException();
    }

    public Task<ClientResponse<IPAccessControlListResponse>> CreateIPAccessControlListAsync(
        Guid? accessControlListId,
        IPAccessControlListRequest request)
    {
        throw new NotImplementedException();
    }

    public Task<ClientResponse<IdentityProviderResponse>> CreateIdentityProviderAsync(
        Guid? identityProviderId,
        IdentityProviderRequest request)
    {
        throw new NotImplementedException();
    }

    public Task<ClientResponse<LambdaResponse>> CreateLambdaAsync(Guid? lambdaId, LambdaRequest request)
    {
        throw new NotImplementedException();
    }

    public Task<ClientResponse<MessageTemplateResponse>> CreateMessageTemplateAsync(
        Guid? messageTemplateId,
        MessageTemplateRequest request)
    {
        throw new NotImplementedException();
    }

    public Task<ClientResponse<MessengerResponse>> CreateMessengerAsync(Guid? messengerId, MessengerRequest request)
    {
        throw new NotImplementedException();
    }

    public Task<ClientResponse<TenantResponse>> CreateTenantAsync(Guid? tenantId, TenantRequest request)
    {
        throw new NotImplementedException();
    }

    public Task<ClientResponse<ThemeResponse>> CreateThemeAsync(Guid? themeId, ThemeRequest request)
    {
        throw new NotImplementedException();
    }

    public Task<ClientResponse<UserResponse>> CreateUserAsync(Guid? userId, UserRequest request)
    {
        throw new NotImplementedException();
    }

    public Task<ClientResponse<UserActionResponse>> CreateUserActionAsync(Guid? userActionId, UserActionRequest request)
    {
        throw new NotImplementedException();
    }

    public Task<ClientResponse<UserActionReasonResponse>> CreateUserActionReasonAsync(
        Guid? userActionReasonId,
        UserActionReasonRequest request)
    {
        throw new NotImplementedException();
    }

    public Task<ClientResponse<UserConsentResponse>> CreateUserConsentAsync(
        Guid? userConsentId,
        UserConsentRequest request)
    {
        throw new NotImplementedException();
    }

    public Task<ClientResponse<IdentityProviderLinkResponse>> CreateUserLinkAsync(IdentityProviderLinkRequest request)
    {
        throw new NotImplementedException();
    }

    public Task<ClientResponse<WebhookResponse>> CreateWebhookAsync(Guid? webhookId, WebhookRequest request)
    {
        throw new NotImplementedException();
    }

    public Task<ClientResponse<RESTVoid>> DeactivateApplicationAsync(Guid? applicationId)
    {
        throw new NotImplementedException();
    }

    public Task<ClientResponse<RESTVoid>> DeactivateReactorAsync()
    {
        throw new NotImplementedException();
    }

    public Task<ClientResponse<RESTVoid>> DeactivateUserAsync(Guid? userId)
    {
        throw new NotImplementedException();
    }

    public Task<ClientResponse<RESTVoid>> DeactivateUserActionAsync(Guid? userActionId)
    {
        throw new NotImplementedException();
    }

    public Task<ClientResponse<UserDeleteResponse>> DeactivateUsersAsync(List<string> userIds)
    {
        throw new NotImplementedException();
    }

    public Task<ClientResponse<UserDeleteResponse>> DeactivateUsersByIdsAsync(List<string> userIds)
    {
        throw new NotImplementedException();
    }

    public Task<ClientResponse<RESTVoid>> DeleteAPIKeyAsync(Guid? keyId)
    {
        throw new NotImplementedException();
    }

    public Task<ClientResponse<RESTVoid>> DeleteApplicationAsync(Guid? applicationId)
    {
        throw new NotImplementedException();
    }

    public Task<ClientResponse<RESTVoid>> DeleteApplicationRoleAsync(Guid? applicationId, Guid? roleId)
    {
        throw new NotImplementedException();
    }

    public Task<ClientResponse<RESTVoid>> DeleteConnectorAsync(Guid? connectorId)
    {
        throw new NotImplementedException();
    }

    public Task<ClientResponse<RESTVoid>> DeleteConsentAsync(Guid? consentId)
    {
        throw new NotImplementedException();
    }

    public Task<ClientResponse<RESTVoid>> DeleteEmailTemplateAsync(Guid? emailTemplateId)
    {
        throw new NotImplementedException();
    }

    public Task<ClientResponse<RESTVoid>> DeleteEntityAsync(Guid? entityId)
    {
        throw new NotImplementedException();
    }

    public Task<ClientResponse<RESTVoid>> DeleteEntityGrantAsync(Guid? entityId, Guid? recipientEntityId, Guid? userId)
    {
        throw new NotImplementedException();
    }

    public Task<ClientResponse<RESTVoid>> DeleteEntityTypeAsync(Guid? entityTypeId)
    {
        throw new NotImplementedException();
    }

    public Task<ClientResponse<RESTVoid>> DeleteEntityTypePermissionAsync(Guid? entityTypeId, Guid? permissionId)
    {
        throw new NotImplementedException();
    }

    public Task<ClientResponse<RESTVoid>> DeleteFormAsync(Guid? formId)
    {
        throw new NotImplementedException();
    }

    public Task<ClientResponse<RESTVoid>> DeleteFormFieldAsync(Guid? fieldId)
    {
        throw new NotImplementedException();
    }

    public Task<ClientResponse<RESTVoid>> DeleteGroupAsync(Guid? groupId)
    {
        throw new NotImplementedException();
    }

    public Task<ClientResponse<RESTVoid>> DeleteGroupMembersAsync(MemberDeleteRequest request)
    {
        throw new NotImplementedException();
    }

    public Task<ClientResponse<RESTVoid>> DeleteIPAccessControlListAsync(Guid? ipAccessControlListId)
    {
        throw new NotImplementedException();
    }

    public Task<ClientResponse<RESTVoid>> DeleteIdentityProviderAsync(Guid? identityProviderId)
    {
        throw new NotImplementedException();
    }

    public Task<ClientResponse<RESTVoid>> DeleteKeyAsync(Guid? keyId)
    {
        throw new NotImplementedException();
    }

    public Task<ClientResponse<RESTVoid>> DeleteLambdaAsync(Guid? lambdaId)
    {
        throw new NotImplementedException();
    }

    public Task<ClientResponse<RESTVoid>> DeleteMessageTemplateAsync(Guid? messageTemplateId)
    {
        throw new NotImplementedException();
    }

    public Task<ClientResponse<RESTVoid>> DeleteMessengerAsync(Guid? messengerId)
    {
        throw new NotImplementedException();
    }

    public Task<ClientResponse<RESTVoid>> DeleteRegistrationAsync(Guid? userId, Guid? applicationId)
    {
        throw new NotImplementedException();
    }

    public Task<ClientResponse<RESTVoid>> DeleteRegistrationWithRequestAsync(
        Guid? userId,
        Guid? applicationId,
        RegistrationDeleteRequest request)
    {
        throw new NotImplementedException();
    }

    public Task<ClientResponse<RESTVoid>> DeleteTenantAsync(Guid? tenantId)
    {
        throw new NotImplementedException();
    }

    public Task<ClientResponse<RESTVoid>> DeleteTenantAsyncAsync(Guid? tenantId)
    {
        throw new NotImplementedException();
    }

    public Task<ClientResponse<RESTVoid>> DeleteTenantWithRequestAsync(Guid? tenantId, TenantDeleteRequest request)
    {
        throw new NotImplementedException();
    }

    public Task<ClientResponse<RESTVoid>> DeleteThemeAsync(Guid? themeId)
    {
        throw new NotImplementedException();
    }

    public Task<ClientResponse<RESTVoid>> DeleteUserAsync(Guid? userId)
    {
        throw new NotImplementedException();
    }

    public Task<ClientResponse<RESTVoid>> DeleteUserActionAsync(Guid? userActionId)
    {
        throw new NotImplementedException();
    }

    public Task<ClientResponse<RESTVoid>> DeleteUserActionReasonAsync(Guid? userActionReasonId)
    {
        throw new NotImplementedException();
    }

    public Task<ClientResponse<IdentityProviderLinkResponse>> DeleteUserLinkAsync(
        Guid? identityProviderId,
        string identityProviderUserId,
        Guid? userId)
    {
        throw new NotImplementedException();
    }

    public Task<ClientResponse<RESTVoid>> DeleteUserWithRequestAsync(Guid? userId, UserDeleteSingleRequest request)
    {
        throw new NotImplementedException();
    }

    public Task<ClientResponse<UserDeleteResponse>> DeleteUsersAsync(UserDeleteRequest request)
    {
        throw new NotImplementedException();
    }

    public Task<ClientResponse<UserDeleteResponse>> DeleteUsersByQueryAsync(UserDeleteRequest request)
    {
        throw new NotImplementedException();
    }

    public Task<ClientResponse<RESTVoid>> DeleteWebhookAsync(Guid? webhookId)
    {
        throw new NotImplementedException();
    }

    public Task<ClientResponse<RESTVoid>> DisableTwoFactorAsync(Guid? userId, string methodId, string code)
    {
        throw new NotImplementedException();
    }

    public Task<ClientResponse<RESTVoid>> DisableTwoFactorWithRequestAsync(
        Guid? userId,
        TwoFactorDisableRequest request)
    {
        throw new NotImplementedException();
    }

    public Task<ClientResponse<TwoFactorResponse>> EnableTwoFactorAsync(Guid? userId, TwoFactorRequest request)
    {
        throw new NotImplementedException();
    }

    [SuppressMessage(
        "Design",
        "CA1054: URI parameters should not be strings",
        Justification = "stubbing 3rd party code")]
    public Task<ClientResponse<AccessToken>> ExchangeOAuthCodeForAccessTokenAsync(
        string code,
        string client_id,
        string client_secret,
        string redirect_uri)
    {
        throw new NotImplementedException();
    }

    [SuppressMessage(
        "Design",
        "CA1054: URI parameters should not be strings",
        Justification = "stubbing 3rd party code")]
    public Task<ClientResponse<AccessToken>> ExchangeOAuthCodeForAccessTokenUsingPKCEAsync(
        string code,
        string client_id,
        string client_secret,
        string redirect_uri,
        string code_verifier)
    {
        throw new NotImplementedException();
    }

    public Task<ClientResponse<AccessToken>> ExchangeRefreshTokenForAccessTokenAsync(
        string refresh_token,
        string client_id,
        string client_secret,
        string scope,
        string user_code)
    {
        throw new NotImplementedException();
    }

    public Task<ClientResponse<JWTRefreshResponse>> ExchangeRefreshTokenForJWTAsync(RefreshRequest request)
    {
        throw new NotImplementedException();
    }

    public Task<ClientResponse<AccessToken>> ExchangeUserCredentialsForAccessTokenAsync(
        string username,
        string password,
        string client_id,
        string client_secret,
        string scope,
        string user_code)
    {
        throw new NotImplementedException();
    }

    public Task<ClientResponse<ForgotPasswordResponse>> ForgotPasswordAsync(ForgotPasswordRequest request)
    {
        throw new NotImplementedException();
    }

    public Task<ClientResponse<VerifyEmailResponse>> GenerateEmailVerificationIdAsync(string email)
    {
        throw new NotImplementedException();
    }

    public Task<ClientResponse<KeyResponse>> GenerateKeyAsync(Guid? keyId, KeyRequest request)
    {
        throw new NotImplementedException();
    }

    public Task<ClientResponse<VerifyRegistrationResponse>> GenerateRegistrationVerificationIdAsync(
        string email,
        Guid? applicationId)
    {
        throw new NotImplementedException();
    }

    public Task<ClientResponse<TwoFactorRecoveryCodeResponse>> GenerateTwoFactorRecoveryCodesAsync(Guid? userId)
    {
        throw new NotImplementedException();
    }

    public Task<ClientResponse<SecretResponse>> GenerateTwoFactorSecretAsync()
    {
        throw new NotImplementedException();
    }

    public Task<ClientResponse<SecretResponse>> GenerateTwoFactorSecretUsingJWTAsync(string encodedJWT)
    {
        throw new NotImplementedException();
    }

    public Task<ClientResponse<LoginResponse>> IdentityProviderLoginAsync(IdentityProviderLoginRequest request)
    {
        throw new NotImplementedException();
    }

    public Task<ClientResponse<KeyResponse>> ImportKeyAsync(Guid? keyId, KeyRequest request)
    {
        throw new NotImplementedException();
    }

    public Task<ClientResponse<RESTVoid>> ImportRefreshTokensAsync(RefreshTokenImportRequest request)
    {
        throw new NotImplementedException();
    }

    public Task<ClientResponse<RESTVoid>> ImportUsersAsync(ImportRequest request)
    {
        throw new NotImplementedException();
    }

    public Task<ClientResponse<IntrospectResponse>> IntrospectAccessTokenAsync(string client_id, string token)
    {
        throw new NotImplementedException();
    }

    public Task<ClientResponse<IssueResponse>> IssueJWTAsync(
        Guid? applicationId,
        string encodedJWT,
        string refreshToken)
    {
        throw new NotImplementedException();
    }

    public Task<ClientResponse<LoginResponse>> LoginAsync(LoginRequest request)
    {
        throw new NotImplementedException();
    }

    public Task<ClientResponse<LoginResponse>> LoginPingAsync(Guid? userId, Guid? applicationId, string callerIPAddress)
    {
        throw new NotImplementedException();
    }

    public Task<ClientResponse<RESTVoid>> LogoutAsync(bool? global, string refreshToken)
    {
        throw new NotImplementedException();
    }

    public Task<ClientResponse<RESTVoid>> LogoutWithRequestAsync(LogoutRequest request)
    {
        throw new NotImplementedException();
    }

    public Task<ClientResponse<LookupResponse>> LookupIdentityProviderAsync(string domain)
    {
        throw new NotImplementedException();
    }

    public Task<ClientResponse<ActionResponse>> ModifyActionAsync(Guid? actionId, ActionRequest request)
    {
        throw new NotImplementedException();
    }

    public Task<ClientResponse<LoginResponse>> PasswordlessLoginAsync(PasswordlessLoginRequest request)
    {
        throw new NotImplementedException();
    }

    public Task<ClientResponse<APIKeyResponse>> PatchAPIKeyAsync(Guid? keyId, APIKeyRequest request)
    {
        throw new NotImplementedException();
    }

    public Task<ClientResponse<ApplicationResponse>> PatchApplicationAsync(
        Guid? applicationId,
        IDictionary<string, object> request)
    {
        throw new NotImplementedException();
    }

    public Task<ClientResponse<ApplicationResponse>> PatchApplicationRoleAsync(
        Guid? applicationId,
        Guid? roleId,
        IDictionary<string, object> request)
    {
        throw new NotImplementedException();
    }

    public Task<ClientResponse<ConnectorResponse>> PatchConnectorAsync(
        Guid? connectorId,
        IDictionary<string, object> request)
    {
        throw new NotImplementedException();
    }

    public Task<ClientResponse<ConsentResponse>> PatchConsentAsync(Guid? consentId, IDictionary<string, object> request)
    {
        throw new NotImplementedException();
    }

    public Task<ClientResponse<EmailTemplateResponse>> PatchEmailTemplateAsync(
        Guid? emailTemplateId,
        IDictionary<string, object> request)
    {
        throw new NotImplementedException();
    }

    public Task<ClientResponse<EntityTypeResponse>> PatchEntityTypeAsync(
        Guid? entityTypeId,
        IDictionary<string, object> request)
    {
        throw new NotImplementedException();
    }

    public Task<ClientResponse<GroupResponse>> PatchGroupAsync(Guid? groupId, IDictionary<string, object> request)
    {
        throw new NotImplementedException();
    }

    public Task<ClientResponse<IdentityProviderResponse>> PatchIdentityProviderAsync(
        Guid? identityProviderId,
        IDictionary<string, object> request)
    {
        throw new NotImplementedException();
    }

    public Task<ClientResponse<IntegrationResponse>> PatchIntegrationsAsync(IDictionary<string, object> request)
    {
        throw new NotImplementedException();
    }

    public Task<ClientResponse<LambdaResponse>> PatchLambdaAsync(Guid? lambdaId, IDictionary<string, object> request)
    {
        throw new NotImplementedException();
    }

    public Task<ClientResponse<MessageTemplateResponse>> PatchMessageTemplateAsync(
        Guid? messageTemplateId,
        IDictionary<string, object> request)
    {
        throw new NotImplementedException();
    }

    public Task<ClientResponse<MessengerResponse>> PatchMessengerAsync(
        Guid? messengerId,
        IDictionary<string, object> request)
    {
        throw new NotImplementedException();
    }

    public Task<ClientResponse<RegistrationResponse>> PatchRegistrationAsync(
        Guid? userId,
        IDictionary<string, object> request)
    {
        throw new NotImplementedException();
    }

    public Task<ClientResponse<SystemConfigurationResponse>> PatchSystemConfigurationAsync(
        IDictionary<string, object> request)
    {
        throw new NotImplementedException();
    }

    public Task<ClientResponse<TenantResponse>> PatchTenantAsync(Guid? tenantId, IDictionary<string, object> request)
    {
        throw new NotImplementedException();
    }

    public Task<ClientResponse<ThemeResponse>> PatchThemeAsync(Guid? themeId, IDictionary<string, object> request)
    {
        throw new NotImplementedException();
    }

    public Task<ClientResponse<UserResponse>> PatchUserAsync(Guid? userId, IDictionary<string, object> request)
    {
        throw new NotImplementedException();
    }

    public Task<ClientResponse<UserActionResponse>> PatchUserActionAsync(
        Guid? userActionId,
        IDictionary<string, object> request)
    {
        throw new NotImplementedException();
    }

    public Task<ClientResponse<UserActionReasonResponse>> PatchUserActionReasonAsync(
        Guid? userActionReasonId,
        IDictionary<string, object> request)
    {
        throw new NotImplementedException();
    }

    public Task<ClientResponse<UserConsentResponse>> PatchUserConsentAsync(
        Guid? userConsentId,
        IDictionary<string, object> request)
    {
        throw new NotImplementedException();
    }

    public Task<ClientResponse<ApplicationResponse>> ReactivateApplicationAsync(Guid? applicationId)
    {
        throw new NotImplementedException();
    }

    public Task<ClientResponse<UserResponse>> ReactivateUserAsync(Guid? userId)
    {
        throw new NotImplementedException();
    }

    public Task<ClientResponse<UserActionResponse>> ReactivateUserActionAsync(Guid? userActionId)
    {
        throw new NotImplementedException();
    }

    public Task<ClientResponse<LoginResponse>> ReconcileJWTAsync(IdentityProviderLoginRequest request)
    {
        throw new NotImplementedException();
    }

    public Task<ClientResponse<RESTVoid>> RefreshEntitySearchIndexAsync()
    {
        throw new NotImplementedException();
    }

    public Task<ClientResponse<RESTVoid>> RefreshUserSearchIndexAsync()
    {
        throw new NotImplementedException();
    }

    public Task<ClientResponse<RESTVoid>> RegenerateReactorKeysAsync()
    {
        throw new NotImplementedException();
    }

    public Task<ClientResponse<RegistrationResponse>> RegisterAsync(Guid? userId, RegistrationRequest request)
    {
        throw new NotImplementedException();
    }

    public Task<ClientResponse<RESTVoid>> ReindexAsync(ReindexRequest request)
    {
        throw new NotImplementedException();
    }

    public Task<ClientResponse<RESTVoid>> RemoveUserFromFamilyAsync(Guid? familyId, Guid? userId)
    {
        throw new NotImplementedException();
    }

    public Task<ClientResponse<VerifyEmailResponse>> ResendEmailVerificationAsync(string email)
    {
        throw new NotImplementedException();
    }

    public Task<ClientResponse<VerifyEmailResponse>> ResendEmailVerificationWithApplicationTemplateAsync(
        Guid? applicationId,
        string email)
    {
        throw new NotImplementedException();
    }

    public Task<ClientResponse<VerifyRegistrationResponse>> ResendRegistrationVerificationAsync(
        string email,
        Guid? applicationId)
    {
        throw new NotImplementedException();
    }

    public Task<ClientResponse<APIKeyResponse>> RetrieveAPIKeyAsync(Guid? keyId)
    {
        throw new NotImplementedException();
    }

    public Task<ClientResponse<ActionResponse>> RetrieveActionAsync(Guid? actionId)
    {
        throw new NotImplementedException();
    }

    public Task<ClientResponse<ActionResponse>> RetrieveActionsAsync(Guid? userId)
    {
        throw new NotImplementedException();
    }

    public Task<ClientResponse<ActionResponse>> RetrieveActionsPreventingLoginAsync(Guid? userId)
    {
        throw new NotImplementedException();
    }

    public Task<ClientResponse<ActionResponse>> RetrieveActiveActionsAsync(Guid? userId)
    {
        throw new NotImplementedException();
    }

    public Task<ClientResponse<ApplicationResponse>> RetrieveApplicationAsync(Guid? applicationId)
    {
        throw new NotImplementedException();
    }

    public Task<ClientResponse<ApplicationResponse>> RetrieveApplicationsAsync()
    {
        throw new NotImplementedException();
    }

    public Task<ClientResponse<AuditLogResponse>> RetrieveAuditLogAsync(int? auditLogId)
    {
        throw new NotImplementedException();
    }

    public Task<ClientResponse<ConnectorResponse>> RetrieveConnectorAsync(Guid? connectorId)
    {
        throw new NotImplementedException();
    }

    public Task<ClientResponse<ConnectorResponse>> RetrieveConnectorsAsync()
    {
        throw new NotImplementedException();
    }

    public Task<ClientResponse<ConsentResponse>> RetrieveConsentAsync(Guid? consentId)
    {
        throw new NotImplementedException();
    }

    public Task<ClientResponse<ConsentResponse>> RetrieveConsentsAsync()
    {
        throw new NotImplementedException();
    }

    public Task<ClientResponse<DailyActiveUserReportResponse>> RetrieveDailyActiveReportAsync(
        Guid? applicationId,
        long? start,
        long? end)
    {
        throw new NotImplementedException();
    }

    public Task<ClientResponse<EmailTemplateResponse>> RetrieveEmailTemplateAsync(Guid? emailTemplateId)
    {
        throw new NotImplementedException();
    }

    public Task<ClientResponse<PreviewResponse>> RetrieveEmailTemplatePreviewAsync(PreviewRequest request)
    {
        throw new NotImplementedException();
    }

    public Task<ClientResponse<EmailTemplateResponse>> RetrieveEmailTemplatesAsync()
    {
        throw new NotImplementedException();
    }

    public Task<ClientResponse<EntityResponse>> RetrieveEntityAsync(Guid? entityId)
    {
        throw new NotImplementedException();
    }

    public Task<ClientResponse<EntityGrantResponse>> RetrieveEntityGrantAsync(
        Guid? entityId,
        Guid? recipientEntityId,
        Guid? userId)
    {
        throw new NotImplementedException();
    }

    public Task<ClientResponse<EntityTypeResponse>> RetrieveEntityTypeAsync(Guid? entityTypeId)
    {
        throw new NotImplementedException();
    }

    public Task<ClientResponse<EntityTypeResponse>> RetrieveEntityTypesAsync()
    {
        throw new NotImplementedException();
    }

    public Task<ClientResponse<EventLogResponse>> RetrieveEventLogAsync(int? eventLogId)
    {
        throw new NotImplementedException();
    }

    public Task<ClientResponse<FamilyResponse>> RetrieveFamiliesAsync(Guid? userId)
    {
        throw new NotImplementedException();
    }

    public Task<ClientResponse<FamilyResponse>> RetrieveFamilyMembersByFamilyIdAsync(Guid? familyId)
    {
        throw new NotImplementedException();
    }

    public Task<ClientResponse<FormResponse>> RetrieveFormAsync(Guid? formId)
    {
        throw new NotImplementedException();
    }

    public Task<ClientResponse<FormFieldResponse>> RetrieveFormFieldAsync(Guid? fieldId)
    {
        throw new NotImplementedException();
    }

    public Task<ClientResponse<FormFieldResponse>> RetrieveFormFieldsAsync()
    {
        throw new NotImplementedException();
    }

    public Task<ClientResponse<FormResponse>> RetrieveFormsAsync()
    {
        throw new NotImplementedException();
    }

    public Task<ClientResponse<GroupResponse>> RetrieveGroupAsync(Guid? groupId)
    {
        throw new NotImplementedException();
    }

    public Task<ClientResponse<GroupResponse>> RetrieveGroupsAsync()
    {
        throw new NotImplementedException();
    }

    public Task<ClientResponse<IPAccessControlListResponse>> RetrieveIPAccessControlListAsync(
        Guid? ipAccessControlListId)
    {
        throw new NotImplementedException();
    }

    public Task<ClientResponse<IdentityProviderResponse>> RetrieveIdentityProviderAsync(Guid? identityProviderId)
    {
        throw new NotImplementedException();
    }

    public Task<ClientResponse<IdentityProviderResponse>> RetrieveIdentityProviderByTypeAsync(IdentityProviderType type)
    {
        throw new NotImplementedException();
    }

    public Task<ClientResponse<IdentityProviderResponse>> RetrieveIdentityProvidersAsync()
    {
        throw new NotImplementedException();
    }

    public Task<ClientResponse<ActionResponse>> RetrieveInactiveActionsAsync(Guid? userId)
    {
        throw new NotImplementedException();
    }

    public Task<ClientResponse<ApplicationResponse>> RetrieveInactiveApplicationsAsync()
    {
        throw new NotImplementedException();
    }

    public Task<ClientResponse<UserActionResponse>> RetrieveInactiveUserActionsAsync()
    {
        throw new NotImplementedException();
    }

    public Task<ClientResponse<IntegrationResponse>> RetrieveIntegrationAsync()
    {
        throw new NotImplementedException();
    }

    public Task<ClientResponse<PublicKeyResponse>> RetrieveJWTPublicKeyAsync(string keyId)
    {
        throw new NotImplementedException();
    }

    public Task<ClientResponse<PublicKeyResponse>> RetrieveJWTPublicKeyByApplicationIdAsync(string applicationId)
    {
        throw new NotImplementedException();
    }

    public Task<ClientResponse<PublicKeyResponse>> RetrieveJWTPublicKeysAsync()
    {
        throw new NotImplementedException();
    }

    public Task<ClientResponse<JWKSResponse>> RetrieveJsonWebKeySetAsync()
    {
        throw new NotImplementedException();
    }

    public Task<ClientResponse<KeyResponse>> RetrieveKeyAsync(Guid? keyId)
    {
        throw new NotImplementedException();
    }

    public Task<ClientResponse<KeyResponse>> RetrieveKeysAsync()
    {
        throw new NotImplementedException();
    }

    public Task<ClientResponse<LambdaResponse>> RetrieveLambdaAsync(Guid? lambdaId)
    {
        throw new NotImplementedException();
    }

    public Task<ClientResponse<LambdaResponse>> RetrieveLambdasAsync()
    {
        throw new NotImplementedException();
    }

    public Task<ClientResponse<LambdaResponse>> RetrieveLambdasByTypeAsync(LambdaType type)
    {
        throw new NotImplementedException();
    }

    public Task<ClientResponse<LoginReportResponse>> RetrieveLoginReportAsync(
        Guid? applicationId,
        long? start,
        long? end)
    {
        throw new NotImplementedException();
    }

    public Task<ClientResponse<MessageTemplateResponse>> RetrieveMessageTemplateAsync(Guid? messageTemplateId)
    {
        throw new NotImplementedException();
    }

    public Task<ClientResponse<PreviewMessageTemplateResponse>> RetrieveMessageTemplatePreviewAsync(
        PreviewMessageTemplateRequest request)
    {
        throw new NotImplementedException();
    }

    public Task<ClientResponse<MessageTemplateResponse>> RetrieveMessageTemplatesAsync()
    {
        throw new NotImplementedException();
    }

    public Task<ClientResponse<MessengerResponse>> RetrieveMessengerAsync(Guid? messengerId)
    {
        throw new NotImplementedException();
    }

    public Task<ClientResponse<MessengerResponse>> RetrieveMessengersAsync()
    {
        throw new NotImplementedException();
    }

    public Task<ClientResponse<MonthlyActiveUserReportResponse>> RetrieveMonthlyActiveReportAsync(
        Guid? applicationId,
        long? start,
        long? end)
    {
        throw new NotImplementedException();
    }

    public Task<ClientResponse<OAuthConfigurationResponse>> RetrieveOauthConfigurationAsync(Guid? applicationId)
    {
        throw new NotImplementedException();
    }

    public Task<ClientResponse<OpenIdConfiguration>> RetrieveOpenIdConfigurationAsync()
    {
        throw new NotImplementedException();
    }

    public Task<ClientResponse<PasswordValidationRulesResponse>> RetrievePasswordValidationRulesAsync()
    {
        throw new NotImplementedException();
    }

    public Task<ClientResponse<PasswordValidationRulesResponse>> RetrievePasswordValidationRulesWithTenantIdAsync(
        Guid? tenantId)
    {
        throw new NotImplementedException();
    }

    public Task<ClientResponse<PendingResponse>> RetrievePendingChildrenAsync(string parentEmail)
    {
        throw new NotImplementedException();
    }

    public Task<ClientResponse<ReactorMetricsResponse>> RetrieveReactorMetricsAsync()
    {
        throw new NotImplementedException();
    }

    public Task<ClientResponse<ReactorResponse>> RetrieveReactorStatusAsync()
    {
        throw new NotImplementedException();
    }

    public Task<ClientResponse<RecentLoginResponse>> RetrieveRecentLoginsAsync(int? offset, int? limit)
    {
        throw new NotImplementedException();
    }

    public Task<ClientResponse<RefreshTokenResponse>> RetrieveRefreshTokenByIdAsync(Guid? userId)
    {
        throw new NotImplementedException();
    }

    public Task<ClientResponse<RefreshTokenResponse>> RetrieveRefreshTokensAsync(Guid? userId)
    {
        throw new NotImplementedException();
    }

    public Task<ClientResponse<RegistrationResponse>> RetrieveRegistrationAsync(Guid? userId, Guid? applicationId)
    {
        throw new NotImplementedException();
    }

    public Task<ClientResponse<RegistrationReportResponse>> RetrieveRegistrationReportAsync(
        Guid? applicationId,
        long? start,
        long? end)
    {
        throw new NotImplementedException();
    }

    public Task<ClientResponse<RESTVoid>> RetrieveReindexStatusAsync()
    {
        throw new NotImplementedException();
    }

    public Task<ClientResponse<SystemConfigurationResponse>> RetrieveSystemConfigurationAsync()
    {
        throw new NotImplementedException();
    }

    public Task<ClientResponse<TenantResponse>> RetrieveTenantAsync(Guid? tenantId)
    {
        throw new NotImplementedException();
    }

    public Task<ClientResponse<TenantResponse>> RetrieveTenantsAsync()
    {
        throw new NotImplementedException();
    }

    public Task<ClientResponse<ThemeResponse>> RetrieveThemeAsync(Guid? themeId)
    {
        throw new NotImplementedException();
    }

    public Task<ClientResponse<ThemeResponse>> RetrieveThemesAsync()
    {
        throw new NotImplementedException();
    }

    public Task<ClientResponse<TotalsReportResponse>> RetrieveTotalReportAsync()
    {
        throw new NotImplementedException();
    }

    public Task<ClientResponse<TwoFactorRecoveryCodeResponse>> RetrieveTwoFactorRecoveryCodesAsync(Guid? userId)
    {
        throw new NotImplementedException();
    }

    public Task<ClientResponse<UserResponse>> RetrieveUserAsync(Guid? userId)
    {
        throw new NotImplementedException();
    }

    public Task<ClientResponse<UserActionResponse>> RetrieveUserActionAsync(Guid? userActionId)
    {
        throw new NotImplementedException();
    }

    public Task<ClientResponse<UserActionReasonResponse>> RetrieveUserActionReasonAsync(Guid? userActionReasonId)
    {
        throw new NotImplementedException();
    }

    public Task<ClientResponse<UserActionReasonResponse>> RetrieveUserActionReasonsAsync()
    {
        throw new NotImplementedException();
    }

    public Task<ClientResponse<UserActionResponse>> RetrieveUserActionsAsync()
    {
        throw new NotImplementedException();
    }

    public Task<ClientResponse<UserResponse>> RetrieveUserByChangePasswordIdAsync(string changePasswordId)
    {
        throw new NotImplementedException();
    }

    public Task<ClientResponse<UserResponse>> RetrieveUserByEmailAsync(string email)
    {
        throw new NotImplementedException();
    }

    public Task<ClientResponse<UserResponse>> RetrieveUserByLoginIdAsync(string loginId)
    {
        throw new NotImplementedException();
    }

    public Task<ClientResponse<UserResponse>> RetrieveUserByUsernameAsync(string username)
    {
        throw new NotImplementedException();
    }

    public Task<ClientResponse<UserResponse>> RetrieveUserByVerificationIdAsync(string verificationId)
    {
        throw new NotImplementedException();
    }

    public Task<ClientResponse<UserCommentResponse>> RetrieveUserCommentsAsync(Guid? userId)
    {
        throw new NotImplementedException();
    }

    public Task<ClientResponse<UserConsentResponse>> RetrieveUserConsentAsync(Guid? userConsentId)
    {
        throw new NotImplementedException();
    }

    public Task<ClientResponse<UserConsentResponse>> RetrieveUserConsentsAsync(Guid? userId)
    {
        throw new NotImplementedException();
    }

    public Task<ClientResponse<UserResponse>> RetrieveUserInfoFromAccessTokenAsync(string encodedJWT)
    {
        throw new NotImplementedException();
    }

    public Task<ClientResponse<IdentityProviderLinkResponse>> RetrieveUserLinkAsync(
        Guid? identityProviderId,
        string identityProviderUserId,
        Guid? userId)
    {
        throw new NotImplementedException();
    }

    public Task<ClientResponse<IdentityProviderLinkResponse>> RetrieveUserLinksByUserIdAsync(
        Guid? identityProviderId,
        Guid? userId)
    {
        throw new NotImplementedException();
    }

    public Task<ClientResponse<LoginReportResponse>> RetrieveUserLoginReportAsync(
        Guid? applicationId,
        Guid? userId,
        long? start,
        long? end)
    {
        throw new NotImplementedException();
    }

    public Task<ClientResponse<LoginReportResponse>> RetrieveUserLoginReportByLoginIdAsync(
        Guid? applicationId,
        string loginId,
        long? start,
        long? end)
    {
        throw new NotImplementedException();
    }

    public Task<ClientResponse<RecentLoginResponse>> RetrieveUserRecentLoginsAsync(
        Guid? userId,
        int? offset,
        int? limit)
    {
        throw new NotImplementedException();
    }

    public Task<ClientResponse<UserResponse>> RetrieveUserUsingJWTAsync(string encodedJWT)
    {
        throw new NotImplementedException();
    }

    public Task<ClientResponse<VersionResponse>> RetrieveVersionAsync()
    {
        throw new NotImplementedException();
    }

    public Task<ClientResponse<WebhookResponse>> RetrieveWebhookAsync(Guid? webhookId)
    {
        throw new NotImplementedException();
    }

    public Task<ClientResponse<WebhookResponse>> RetrieveWebhooksAsync()
    {
        throw new NotImplementedException();
    }

    public Task<ClientResponse<RESTVoid>> RevokeRefreshTokenAsync(string token, Guid? userId, Guid? applicationId)
    {
        throw new NotImplementedException();
    }

    public Task<ClientResponse<RESTVoid>> RevokeRefreshTokenByIdAsync(Guid? tokenId)
    {
        throw new NotImplementedException();
    }

    public Task<ClientResponse<RESTVoid>> RevokeRefreshTokenByTokenAsync(string token)
    {
        throw new NotImplementedException();
    }

    public Task<ClientResponse<RESTVoid>> RevokeRefreshTokensByApplicationIdAsync(Guid? applicationId)
    {
        throw new NotImplementedException();
    }

    public Task<ClientResponse<RESTVoid>> RevokeRefreshTokensByUserIdAsync(Guid? userId)
    {
        throw new NotImplementedException();
    }

    public Task<ClientResponse<RESTVoid>> RevokeRefreshTokensByUserIdForApplicationAsync(
        Guid? userId,
        Guid? applicationId)
    {
        throw new NotImplementedException();
    }

    public Task<ClientResponse<RESTVoid>> RevokeRefreshTokensWithRequestAsync(RefreshTokenRevokeRequest request)
    {
        throw new NotImplementedException();
    }

    public Task<ClientResponse<RESTVoid>> RevokeUserConsentAsync(Guid? userConsentId)
    {
        throw new NotImplementedException();
    }

    public Task<ClientResponse<AuditLogSearchResponse>> SearchAuditLogsAsync(AuditLogSearchRequest request)
    {
        throw new NotImplementedException();
    }

    public Task<ClientResponse<EntitySearchResponse>> SearchEntitiesAsync(EntitySearchRequest request)
    {
        throw new NotImplementedException();
    }

    public Task<ClientResponse<EntitySearchResponse>> SearchEntitiesByIdsAsync(List<string> ids)
    {
        throw new NotImplementedException();
    }

    public Task<ClientResponse<EntityGrantSearchResponse>> SearchEntityGrantsAsync(EntityGrantSearchRequest request)
    {
        throw new NotImplementedException();
    }

    public Task<ClientResponse<EntityTypeSearchResponse>> SearchEntityTypesAsync(EntityTypeSearchRequest request)
    {
        throw new NotImplementedException();
    }

    public Task<ClientResponse<EventLogSearchResponse>> SearchEventLogsAsync(EventLogSearchRequest request)
    {
        throw new NotImplementedException();
    }

    public Task<ClientResponse<IPAccessControlListSearchResponse>> SearchIPAccessControlListsAsync(
        IPAccessControlListSearchRequest request)
    {
        throw new NotImplementedException();
    }

    public Task<ClientResponse<LoginRecordSearchResponse>> SearchLoginRecordsAsync(LoginRecordSearchRequest request)
    {
        throw new NotImplementedException();
    }

    public Task<ClientResponse<SearchResponse>> SearchUsersAsync(List<string> ids)
    {
        throw new NotImplementedException();
    }

    public Task<ClientResponse<SearchResponse>> SearchUsersByIdsAsync(List<string> ids)
    {
        throw new NotImplementedException();
    }

    public Task<ClientResponse<SearchResponse>> SearchUsersByQueryAsync(SearchRequest request)
    {
        throw new NotImplementedException();
    }

    public Task<ClientResponse<SearchResponse>> SearchUsersByQueryStringAsync(SearchRequest request)
    {
        throw new NotImplementedException();
    }

    public Task<ClientResponse<SendResponse>> SendEmailAsync(Guid? emailTemplateId, SendRequest request)
    {
        throw new NotImplementedException();
    }

    public Task<ClientResponse<RESTVoid>> SendFamilyRequestEmailAsync(FamilyEmailRequest request)
    {
        throw new NotImplementedException();
    }

    public Task<ClientResponse<RESTVoid>> SendPasswordlessCodeAsync(PasswordlessSendRequest request)
    {
        throw new NotImplementedException();
    }

    public Task<ClientResponse<RESTVoid>> SendTwoFactorCodeAsync(TwoFactorSendRequest request)
    {
        throw new NotImplementedException();
    }

    public Task<ClientResponse<RESTVoid>> SendTwoFactorCodeForEnableDisableAsync(TwoFactorSendRequest request)
    {
        throw new NotImplementedException();
    }

    public Task<ClientResponse<RESTVoid>> SendTwoFactorCodeForLoginAsync(string twoFactorId)
    {
        throw new NotImplementedException();
    }

    public Task<ClientResponse<RESTVoid>> SendTwoFactorCodeForLoginUsingMethodAsync(
        string twoFactorId,
        TwoFactorSendRequest request)
    {
        throw new NotImplementedException();
    }

    public Task<ClientResponse<IdentityProviderStartLoginResponse>> StartIdentityProviderLoginAsync(
        IdentityProviderStartLoginRequest request)
    {
        throw new NotImplementedException();
    }

    public Task<ClientResponse<PasswordlessStartResponse>> StartPasswordlessLoginAsync(PasswordlessStartRequest request)
    {
        throw new NotImplementedException();
    }

    public Task<ClientResponse<TwoFactorStartResponse>> StartTwoFactorLoginAsync(TwoFactorStartRequest request)
    {
        throw new NotImplementedException();
    }

    public Task<ClientResponse<LoginResponse>> TwoFactorLoginAsync(TwoFactorLoginRequest request)
    {
        throw new NotImplementedException();
    }

    public Task<ClientResponse<APIKeyResponse>> UpdateAPIKeyAsync(Guid? apiKeyId, APIKeyRequest request)
    {
        throw new NotImplementedException();
    }

    public Task<ClientResponse<ApplicationResponse>> UpdateApplicationAsync(
        Guid? applicationId,
        ApplicationRequest request)
    {
        throw new NotImplementedException();
    }

    public Task<ClientResponse<ApplicationResponse>> UpdateApplicationRoleAsync(
        Guid? applicationId,
        Guid? roleId,
        ApplicationRequest request)
    {
        throw new NotImplementedException();
    }

    public Task<ClientResponse<ConnectorResponse>> UpdateConnectorAsync(Guid? connectorId, ConnectorRequest request)
    {
        throw new NotImplementedException();
    }

    public Task<ClientResponse<ConsentResponse>> UpdateConsentAsync(Guid? consentId, ConsentRequest request)
    {
        throw new NotImplementedException();
    }

    public Task<ClientResponse<EmailTemplateResponse>> UpdateEmailTemplateAsync(
        Guid? emailTemplateId,
        EmailTemplateRequest request)
    {
        throw new NotImplementedException();
    }

    public Task<ClientResponse<EntityResponse>> UpdateEntityAsync(Guid? entityId, EntityRequest request)
    {
        throw new NotImplementedException();
    }

    public Task<ClientResponse<EntityTypeResponse>> UpdateEntityTypeAsync(Guid? entityTypeId, EntityTypeRequest request)
    {
        throw new NotImplementedException();
    }

    public Task<ClientResponse<EntityTypeResponse>> UpdateEntityTypePermissionAsync(
        Guid? entityTypeId,
        Guid? permissionId,
        EntityTypeRequest request)
    {
        throw new NotImplementedException();
    }

    public Task<ClientResponse<FormResponse>> UpdateFormAsync(Guid? formId, FormRequest request)
    {
        throw new NotImplementedException();
    }

    public Task<ClientResponse<FormFieldResponse>> UpdateFormFieldAsync(Guid? fieldId, FormFieldRequest request)
    {
        throw new NotImplementedException();
    }

    public Task<ClientResponse<GroupResponse>> UpdateGroupAsync(Guid? groupId, GroupRequest request)
    {
        throw new NotImplementedException();
    }

    public Task<ClientResponse<IPAccessControlListResponse>> UpdateIPAccessControlListAsync(
        Guid? accessControlListId,
        IPAccessControlListRequest request)
    {
        throw new NotImplementedException();
    }

    public Task<ClientResponse<IdentityProviderResponse>> UpdateIdentityProviderAsync(
        Guid? identityProviderId,
        IdentityProviderRequest request)
    {
        throw new NotImplementedException();
    }

    public Task<ClientResponse<IntegrationResponse>> UpdateIntegrationsAsync(IntegrationRequest request)
    {
        throw new NotImplementedException();
    }

    public Task<ClientResponse<KeyResponse>> UpdateKeyAsync(Guid? keyId, KeyRequest request)
    {
        throw new NotImplementedException();
    }

    public Task<ClientResponse<LambdaResponse>> UpdateLambdaAsync(Guid? lambdaId, LambdaRequest request)
    {
        throw new NotImplementedException();
    }

    public Task<ClientResponse<MessageTemplateResponse>> UpdateMessageTemplateAsync(
        Guid? messageTemplateId,
        MessageTemplateRequest request)
    {
        throw new NotImplementedException();
    }

    public Task<ClientResponse<MessengerResponse>> UpdateMessengerAsync(Guid? messengerId, MessengerRequest request)
    {
        throw new NotImplementedException();
    }

    public Task<ClientResponse<RegistrationResponse>> UpdateRegistrationAsync(Guid? userId, RegistrationRequest request)
    {
        throw new NotImplementedException();
    }

    public Task<ClientResponse<SystemConfigurationResponse>> UpdateSystemConfigurationAsync(
        SystemConfigurationRequest request)
    {
        throw new NotImplementedException();
    }

    public Task<ClientResponse<TenantResponse>> UpdateTenantAsync(Guid? tenantId, TenantRequest request)
    {
        throw new NotImplementedException();
    }

    public Task<ClientResponse<ThemeResponse>> UpdateThemeAsync(Guid? themeId, ThemeRequest request)
    {
        throw new NotImplementedException();
    }

    public Task<ClientResponse<UserResponse>> UpdateUserAsync(Guid? userId, UserRequest request)
    {
        throw new NotImplementedException();
    }

    public Task<ClientResponse<UserActionResponse>> UpdateUserActionAsync(Guid? userActionId, UserActionRequest request)
    {
        throw new NotImplementedException();
    }

    public Task<ClientResponse<UserActionReasonResponse>> UpdateUserActionReasonAsync(
        Guid? userActionReasonId,
        UserActionReasonRequest request)
    {
        throw new NotImplementedException();
    }

    public Task<ClientResponse<UserConsentResponse>> UpdateUserConsentAsync(
        Guid? userConsentId,
        UserConsentRequest request)
    {
        throw new NotImplementedException();
    }

    public Task<ClientResponse<WebhookResponse>> UpdateWebhookAsync(Guid? webhookId, WebhookRequest request)
    {
        throw new NotImplementedException();
    }

    public Task<ClientResponse<RESTVoid>> UpsertEntityGrantAsync(Guid? entityId, EntityGrantRequest request)
    {
        throw new NotImplementedException();
    }

    public Task<ClientResponse<RESTVoid>> ValidateDeviceAsync(string user_code, string client_id)
    {
        throw new NotImplementedException();
    }

    public Task<ClientResponse<ValidateResponse>> ValidateJWTAsync(string encodedJWT)
    {
        throw new NotImplementedException();
    }

    public Task<ClientResponse<JWTVendResponse>> VendJWTAsync(JWTVendRequest request)
    {
        throw new NotImplementedException();
    }

    public Task<ClientResponse<RESTVoid>> VerifyEmailAsync(string verificationId)
    {
        throw new NotImplementedException();
    }

    public Task<ClientResponse<RESTVoid>> VerifyEmailAddressAsync(VerifyEmailRequest request)
    {
        throw new NotImplementedException();
    }

    public Task<ClientResponse<RESTVoid>> VerifyRegistrationAsync(string verificationId)
    {
        throw new NotImplementedException();
    }

    public Task<ClientResponse<RESTVoid>> VerifyUserRegistrationAsync(VerifyRegistrationRequest request)
    {
        throw new NotImplementedException();
    }
}
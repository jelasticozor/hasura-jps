namespace HasuraFunction;

using System.Threading.Tasks;
using AutoMapper;
using io.fusionauth;
using io.fusionauth.domain.api;
using Microsoft.AspNetCore.DataProtection;
using Microsoft.Extensions.Logging;
using Softozor.HasuraHandling.Exceptions;
using Softozor.HasuraHandling.Interfaces;

public class LoginHandler : IActionHandler<LoginInput, (LoginOutput, string)>
{
    private readonly IFusionAuthAsyncClient authClient;

    private readonly ILogger<LoginHandler> logger;

    private readonly IMapper mapper;

    private readonly IDataProtector protector;

    public LoginHandler(
        IDataProtector protector,
        IFusionAuthAsyncClient authClient,
        ILogger<LoginHandler> logger,
        IMapper mapper)
    {
        this.protector = protector;
        this.authClient = authClient;
        this.logger = logger;
        this.mapper = mapper;
    }

    public async Task<(LoginOutput, string)> Handle(LoginInput input)
    {
        var request = this.mapper.Map<LoginInput, LoginRequest>(input);

        var response = await this.authClient.LoginAsync(request);

        if (response.WasSuccessful())
        {
            this.logger.LogInformation($"Successful login for user {input.Username} on application {input.AppId}");

            var protectedRefreshToken = this.protector.Protect(response.successResponse.refreshToken);

            return (this.mapper.Map<LoginResponse, LoginOutput>(response.successResponse), protectedRefreshToken);
        }

        var errorMsg = $"Unable to log in user {input.Username} on application {input.AppId}";
        throw new HasuraFunctionException(errorMsg, response.statusCode, response.exception);
    }
}
namespace HasuraFunction;

using System.Threading.Tasks;
using AutoMapper;
using io.fusionauth;
using io.fusionauth.domain.api;
using Microsoft.AspNetCore.DataProtection;
using Microsoft.AspNetCore.Http;
using Microsoft.Extensions.Logging;
using Softozor.HasuraHandling.Exceptions;
using Softozor.HasuraHandling.Interfaces;

public class SignInHandler : IActionHandler<SignInInput, (SignInOutput, string)>
{
    private readonly IFusionAuthAsyncClient authClient;

    private readonly ILogger<SignInHandler> logger;

    private readonly IMapper mapper;

    private readonly IDataProtector protector;

    public SignInHandler(
        IDataProtector protector,
        IFusionAuthAsyncClient authClient,
        ILogger<SignInHandler> logger,
        IMapper mapper)
    {
        this.protector = protector;
        this.authClient = authClient;
        this.logger = logger;
        this.mapper = mapper;
    }

    public async Task<(SignInOutput, string)> Handle(SignInInput input)
    {
        var request = this.mapper.Map<SignInInput, LoginRequest>(input);

        var response = await this.authClient.LoginAsync(request);

        if (response.WasSuccessful())
        {
            this.logger.LogInformation($"Successful login for user {input.Username} on application {input.AppId}");

            if (response.successResponse.refreshToken is null)
            {
                throw new HasuraFunctionException(
                    $"No refresh token for user {input.Username} on application {input.AppId}", StatusCodes.Status401Unauthorized);
            }

            var protectedRefreshToken = this.protector.Protect(response.successResponse.refreshToken);

            return (this.mapper.Map<LoginResponse, SignInOutput>(response.successResponse), protectedRefreshToken);
        }

        throw new HasuraFunctionException(
            $"Unable to log in user {input.Username} on application {input.AppId}", response.statusCode, response.exception);
    }
}
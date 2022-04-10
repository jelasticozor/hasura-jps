namespace HasuraFunction;

using System.Threading.Tasks;
using AutoMapper;
using io.fusionauth;
using io.fusionauth.domain.api;
using Microsoft.AspNetCore.Http;
using Microsoft.Extensions.Logging;
using Softozor.HasuraHandling;

public class SignInHandler
{
    private readonly IFusionAuthAsyncClient authClient;

    private readonly ILogger<SignInHandler> logger;

    private readonly IMapper mapper;

    public SignInHandler(IFusionAuthAsyncClient authClient, ILogger<SignInHandler> logger, IMapper mapper)
    {
        this.authClient = authClient;
        this.logger = logger;
        this.mapper = mapper;
    }

    public async Task<SignInOutput> Handle(SignInInput input)
    {
        var request = this.mapper.Map<SignInInput, LoginRequest>(input);

        var response = await this.authClient.LoginAsync(request);

        if (!response.WasSuccessful())
        {
            throw new HasuraFunctionException(
                $"Unable to sign user {input.Username} on application {input.AppId}",
                response.statusCode,
                response.exception);
        }

        this.logger.LogInformation(
            "Successful signin for user {Username} on application {AppId}",
            input.Username,
            input.AppId);

        if (response.successResponse.refreshToken is null)
        {
            throw new HasuraFunctionException(
                $"No refresh token for user {input.Username} on application {input.AppId}",
                StatusCodes.Status401Unauthorized);
        }

        return this.mapper.Map<LoginResponse, SignInOutput>(response.successResponse);
    }
}
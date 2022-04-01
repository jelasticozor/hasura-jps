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

public class SignUpHandler : IActionHandler<SignUpInput, SignUpOutput>
{
    private readonly IFusionAuthAsyncClient authClient;

    private readonly ILogger<SignUpHandler> logger;

    private readonly IMapper mapper;

    public SignUpHandler(
        IFusionAuthAsyncClient authClient,
        ILogger<SignUpHandler> logger,
        IMapper mapper)
    {
        this.authClient = authClient;
        this.logger = logger;
        this.mapper = mapper;
    }

    public Task<SignUpOutput> Handle(SignUpInput input)
    {
        // var request = this.mapper.Map<SignUpInput, LoginRequest>(input);
        //
        // var response = await this.authClient.LoginAsync(request);
        //
        // if (response.WasSuccessful())
        // {
        //     this.logger.LogInformation($"Successful signin for user {input.Username} on application {input.AppId}");
        //
        //     if (response.successResponse.refreshToken is null)
        //     {
        //         throw new HasuraFunctionException(
        //             $"No refresh token for user {input.Username} on application {input.AppId}", StatusCodes.Status401Unauthorized);
        //     }
        //
        //     var protectedRefreshToken = this.protector.Protect(response.successResponse.refreshToken);
        //
        //     return (this.mapper.Map<LoginResponse, SignUpOutput>(response.successResponse), protectedRefreshToken);
        // }

        // throw new HasuraFunctionException(
        //     $"Unable to sign user {input.Email} on application {input.AppId}", response.statusCode, response.exception);

        throw new HasuraFunctionException(
            $"Unable to sign user {input.Email} on application {input.AppId}");
    }
}
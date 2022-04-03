namespace HasuraFunction;

using System.Threading.Tasks;
using AutoMapper;
using io.fusionauth;
using Microsoft.Extensions.Logging;
using Softozor.HasuraHandling.Exceptions;
using Softozor.HasuraHandling.Interfaces;

public class SetPasswordHandler : IActionHandler<SetPasswordInput, SetPasswordOutput>
{
    private readonly IFusionAuthAsyncClient authClient;

    private readonly ILogger<SetPasswordHandler> logger;

    private readonly IMapper mapper;

    public SetPasswordHandler(IFusionAuthAsyncClient authClient, ILogger<SetPasswordHandler> logger, IMapper mapper)
    {
        this.authClient = authClient;
        this.logger = logger;
        this.mapper = mapper;
    }

    public Task<SetPasswordOutput> Handle(SetPasswordInput input)
    {
        // var request = this.mapper.Map<SetPasswordInput, LoginRequest>(input);
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
        //     return (this.mapper.Map<LoginResponse, SetPasswordOutput>(response.successResponse), protectedRefreshToken);
        // }

        // throw new HasuraFunctionException(
        //     $"Unable to sign user {input.Username} on application {input.AppId}", response.statusCode, response.exception);
        throw new HasuraFunctionException("Unable to set password");
    }
}
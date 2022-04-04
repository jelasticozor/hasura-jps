namespace HasuraFunction;

using System.Threading.Tasks;
using AutoMapper;
using io.fusionauth;
using io.fusionauth.domain.api;
using io.fusionauth.domain.api.user;
using Microsoft.AspNetCore.Http;
using Microsoft.Extensions.Logging;
using Softozor.HasuraHandling.Exceptions;
using Softozor.HasuraHandling.Interfaces;

public class SetPasswordHandler
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

    public async Task Handle(SetPasswordInput input)
    {
        var request = this.mapper.Map<SetPasswordInput, ChangePasswordRequest>(input);

        var response = await this.authClient.ChangePasswordAsync(input.ChangePasswordId, request);

        if (!response.WasSuccessful())
        {
            throw new HasuraFunctionException(
                $"Unable to set password with change password id {input.ChangePasswordId}", response.statusCode, response.exception);
        }

        this.logger.LogInformation($"Successfully set password");
    }
}
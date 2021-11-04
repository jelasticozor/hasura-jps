namespace HasuraFunction;

using System.Threading.Tasks;
using AutoMapper;
using io.fusionauth;
using io.fusionauth.domain.api.jwt;
using Microsoft.Extensions.Logging;
using Softozor.HasuraHandling.Exceptions;
using Softozor.HasuraHandling.Interfaces;

public class ValidateTokenHandler : IActionHandler<BearerTokenAuthorizationHeader, ValidateTokenOutput>
{
    private readonly IFusionAuthAsyncClient authClient;

    private readonly ILogger<ValidateTokenHandler> logger;

    private readonly IMapper mapper;

    public ValidateTokenHandler(IFusionAuthAsyncClient authClient, ILogger<ValidateTokenHandler> logger, IMapper mapper)
    {
        this.authClient = authClient;
        this.logger = logger;
        this.mapper = mapper;
    }

    public async Task<ValidateTokenOutput> Handle(BearerTokenAuthorizationHeader input)
    {
        var token = input.Token;

        var response = await this.authClient.ValidateJWTAsync(token);

        if (response.WasSuccessful())
        {
            this.logger.LogInformation($"Token {token} is valid");

            return this.mapper.Map<ValidateResponse, ValidateTokenOutput>(response.successResponse);
        }

        var errorMsg = $"Unable to validate token {token}";
        throw new HasuraFunctionException(errorMsg, response.statusCode, response.exception);
    }
}
namespace HasuraFunction;

using System.Threading.Tasks;
using AutoMapper;
using io.fusionauth;
using io.fusionauth.domain.api.jwt;
using Microsoft.Extensions.Logging;
using Softozor.HasuraHandling;

public class ValidateTokenHandler
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

        if (!response.WasSuccessful())
        {
            throw new HasuraFunctionException(
                $"Unable to validate token {token}",
                response.statusCode,
                response.exception);
        }

        this.logger.LogInformation("Token {Token} is valid", token);

        return this.mapper.Map<ValidateResponse, ValidateTokenOutput>(response.successResponse);
    }
}
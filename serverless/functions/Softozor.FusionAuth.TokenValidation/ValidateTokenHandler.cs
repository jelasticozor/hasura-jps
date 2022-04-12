namespace HasuraFunction;

using System.Threading.Tasks;
using io.fusionauth;
using Softozor.HasuraHandling;

public class ValidateTokenHandler
{
    private readonly IFusionAuthAsyncClient authClient;

    public ValidateTokenHandler(IFusionAuthAsyncClient authClient)
    {
        this.authClient = authClient;
    }

    public async Task Handle(BearerTokenAuthorizationHeader input)
    {
        var response = await this.authClient.ValidateJWTAsync(input.Token);

        if (!response.WasSuccessful())
        {
            throw new HasuraFunctionException(
                $"Unable to validate token {input.Token}",
                response.statusCode,
                response.exception);
        }
    }
}
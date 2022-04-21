namespace HasuraFunction;

using System.Globalization;
using System.Threading.Tasks;
using AutoMapper;
using io.fusionauth;
using io.fusionauth.domain.api.jwt;
using Softozor.HasuraHandling;

public class RefreshJwtHandler
{
    private readonly IFusionAuthAsyncClient authClient;

    private readonly IMapper mapper;

    public RefreshJwtHandler(IFusionAuthAsyncClient authClient, IMapper mapper)
    {
        this.authClient = authClient;
        this.mapper = mapper;
    }

    public async Task<RefreshJwtOutput> Handle(RefreshJwtInput input, string token)
    {
        var request = new RefreshRequest { token = token, refreshToken = input.RefreshToken };

        var response = await this.authClient.ExchangeRefreshTokenForJWTAsync(request);

        if (!response.WasSuccessful())
        {
            throw new HasuraFunctionException(
                string.Format(CultureInfo.InvariantCulture, "Unable to refresh JWT"),
                response.statusCode,
                response.exception);
        }

        return this.mapper.Map<JWTRefreshResponse, RefreshJwtOutput>(response.successResponse);
    }
}
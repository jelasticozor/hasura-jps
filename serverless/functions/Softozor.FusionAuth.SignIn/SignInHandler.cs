namespace HasuraFunction;

using System.Globalization;
using System.Threading.Tasks;
using AutoMapper;
using io.fusionauth;
using io.fusionauth.domain.api;
using Softozor.HasuraHandling;

public class SignInHandler
{
    private readonly IFusionAuthAsyncClient authClient;

    private readonly IMapper mapper;

    public SignInHandler(IFusionAuthAsyncClient authClient, IMapper mapper)
    {
        this.authClient = authClient;
        this.mapper = mapper;
    }

    public async Task<SignInOutput> Handle(SignInInput input)
    {
        var request = this.mapper.Map<SignInInput, LoginRequest>(input);

        var response = await this.authClient.LoginAsync(request);

        if (!response.WasSuccessful())
        {
            throw new HasuraFunctionException(
                string.Format(
                    CultureInfo.InvariantCulture,
                    "Unable to sign user {0} on application {1}",
                    input.Username,
                    input.AppId),
                response.statusCode,
                response.exception);
        }

        return this.mapper.Map<LoginResponse, SignInOutput>(response.successResponse);
    }
}
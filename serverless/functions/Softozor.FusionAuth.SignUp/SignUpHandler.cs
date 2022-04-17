namespace HasuraFunction;

using System.Globalization;
using System.Threading.Tasks;
using AutoMapper;
using io.fusionauth;
using io.fusionauth.domain.api.user;
using Softozor.HasuraHandling;

public class SignUpHandler
{
    private readonly IFusionAuthAsyncClient authClient;

    private readonly IMapper mapper;

    public SignUpHandler(IFusionAuthAsyncClient authClient, IMapper mapper)
    {
        this.authClient = authClient;
        this.mapper = mapper;
    }

    public async Task<SignUpOutput> Handle(SignUpInput input)
    {
        var request = this.mapper.Map<SignUpInput, RegistrationRequest>(input);

        var response = await this.authClient.RegisterAsync(null, request);

        if (!response.WasSuccessful())
        {
            throw new HasuraFunctionException(
                string.Format(
                    CultureInfo.InvariantCulture,
                    "Unable to sign up user {0} on application {1} with role {2}",
                    input.Email,
                    input.AppId,
                    input.Roles),
                response.statusCode,
                response.exception);
        }

        return this.mapper.Map<RegistrationResponse, SignUpOutput>(response.successResponse);
    }
}
namespace HasuraFunction;

using System.Threading.Tasks;
using AutoMapper;
using io.fusionauth;
using io.fusionauth.domain.api.user;
using Softozor.HasuraHandling;

public class SetPasswordHandler
{
    private readonly IFusionAuthAsyncClient authClient;

    private readonly IMapper mapper;

    public SetPasswordHandler(IFusionAuthAsyncClient authClient, IMapper mapper)
    {
        this.authClient = authClient;
        this.mapper = mapper;
    }

    public async Task Handle(SetPasswordInput input)
    {
        var request = this.mapper.Map<SetPasswordInput, ChangePasswordRequest>(input);

        var response = await this.authClient.ChangePasswordAsync(input.ChangePasswordId, request);

        if (!response.WasSuccessful())
        {
            throw new HasuraFunctionException(
                $"Unable to set password with change password id {input.ChangePasswordId}",
                response.statusCode,
                response.exception);
        }
    }
}
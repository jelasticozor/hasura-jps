namespace HasuraFunction;

using AutoMapper;
using io.fusionauth.domain.api;

public class LoginRequestTypeConverter : ITypeConverter<LoginInput, LoginRequest>
{
    public LoginRequest Convert(LoginInput source, LoginRequest? destination, ResolutionContext context)
    {
        return new LoginRequest { applicationId = source.AppId, loginId = source.Username, password = source.Password };
    }
}
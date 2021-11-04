namespace HasuraFunction;

using AutoMapper;
using io.fusionauth.domain.api;

public class LoginOutputTypeConverter : ITypeConverter<LoginResponse, LoginOutput>
{
    public LoginOutput Convert(LoginResponse source, LoginOutput? destination, ResolutionContext context)
    {
        return new LoginOutput(source.token, source.user.id.GetValueOrDefault());
    }
}
namespace HasuraFunction;

using AutoMapper;
using io.fusionauth.domain.api;

public class LoginProfile : Profile
{
    public LoginProfile()
    {
        this.CreateMap<LoginInput, LoginRequest>().ConvertUsing<LoginRequestTypeConverter>();
        this.CreateMap<LoginResponse, LoginOutput>().ConvertUsing<LoginOutputTypeConverter>();
    }
}
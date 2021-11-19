namespace HasuraFunction;

using AutoMapper;
using io.fusionauth.domain.api;

public class LoginProfile : Profile
{
    public LoginProfile()
    {
        this.CreateMap<LoginInput, LoginRequest>()
            .ForMember(dest => dest.applicationId, opt => opt.MapFrom(src => src.AppId))
            .ForMember(dest => dest.loginId, opt => opt.MapFrom(src => src.Username))
            .ForMember(dest => dest.password, opt => opt.MapFrom(src => src.Password));

        this.CreateMap<LoginResponse, LoginOutput>()
            .ForMember(dest => dest.Token, opt => opt.MapFrom(src => src.token))
            .ForMember(dest => dest.UserId, opt => opt.MapFrom(src => src.user.id.GetValueOrDefault()));
    }
}
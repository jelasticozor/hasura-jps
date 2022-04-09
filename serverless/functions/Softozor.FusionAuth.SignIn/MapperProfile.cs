namespace HasuraFunction;

using AutoMapper;
using io.fusionauth.domain.api;

public class MapperProfile : Profile
{
    public MapperProfile()
    {
        this.CreateMap<SignInInput, LoginRequest>()
            .ForMember(dest => dest.applicationId, opt => opt.MapFrom(src => src.AppId))
            .ForMember(dest => dest.loginId, opt => opt.MapFrom(src => src.Username))
            .ForMember(dest => dest.password, opt => opt.MapFrom(src => src.Password));

        this.CreateMap<LoginResponse, SignInOutput>()
            .ForMember(dest => dest.RefreshToken, opt => opt.MapFrom(src => src.refreshToken))
            .ForMember(dest => dest.Token, opt => opt.MapFrom(src => src.token))
            .ForMember(dest => dest.UserId, opt => opt.MapFrom(src => src.user.id.GetValueOrDefault()));
    }
}
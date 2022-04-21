namespace HasuraFunction;

using AutoMapper;
using io.fusionauth.domain.api;
using io.fusionauth.domain.api.jwt;

public class MapperProfile : Profile
{
    public MapperProfile()
    {
        this.CreateMap<JWTRefreshResponse, RefreshJwtOutput>()
            .ForMember(dest => dest.RefreshToken, opt => opt.MapFrom(src => src.refreshToken))
            .ForMember(dest => dest.Token, opt => opt.MapFrom(src => src.token));
    }
}
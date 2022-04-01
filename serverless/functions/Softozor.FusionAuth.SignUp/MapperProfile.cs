namespace HasuraFunction;

using System.Collections.Generic;
using AutoMapper;
using io.fusionauth.domain;
using io.fusionauth.domain.api.user;

public class MapperProfile : Profile
{
    public MapperProfile()
    {
        // TODO: can this be made in a simpler way?
        this.CreateMap<SignUpInput, RegistrationRequest>()
            .ForMember(dest => dest.sendSetPasswordEmail, opt => opt.MapFrom(_ => true))
            .ForMember(dest => dest.user, opt => opt.MapFrom(src => new User { email = src.Email }))
            .ForMember(
                dest => dest.registration,
                opt => opt.MapFrom(
                    src => new UserRegistration { applicationId = src.AppId, roles = new List<string> { src.Role } }));

        this.CreateMap<RegistrationResponse, SignUpOutput>()
            .ForMember(dest => dest.Token, opt => opt.MapFrom(src => src.token))
            .ForMember(dest => dest.UserId, opt => opt.MapFrom(src => src.user.id));
    }
}
interface Pokemon {
    id: number
    name: string
    artwork: string
}

async function getPokemon(id: string) {
    const response = await fetch(`http://localhost:8080/pokemon/${id}`);
    const data: Pokemon = await response.json();
    return data;
}

export default async function PokemonPage({ params }: any) {
    const pokemon: Pokemon = await getPokemon(params.id);
    return (
        <div className="flex flex-col items-center">
            <img src={pokemon.artwork}></img>
            <p className="text-white">#{pokemon.id}</p>
            <p className="text-white">{pokemon.name}</p>
        </div>
    )
}

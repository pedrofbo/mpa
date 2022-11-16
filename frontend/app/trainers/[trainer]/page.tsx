import Link from "next/link";
import { endpoint } from "../../backend_endpoint";

interface Trainer {
    name: string
    image: string
    registered_at: string
}

async function getTrainer(trainer: string): Promise<Trainer> {
    const response = await fetch(`${endpoint}/trainers/${trainer}`);
    const data: Trainer = await response.json();
    return data;
}

interface Pokemon {
    id: number
    name: string
    nickname?: string
    level?: number
    caught_at?: string
    artwork: string
}

interface TrainerPokemon {
    name: string
    pokemon: Pokemon[]
}

async function getTrainerPokemon(trainer: string): Promise<TrainerPokemon> {
    const response = await fetch(`${endpoint}/trainers/${trainer}/pokemon`);
    const data: TrainerPokemon = await response.json();
    console.log(data);
    return data;
}

async function getRandomPokemon(): Promise<Pokemon> {
    const response = await fetch(`${endpoint}/pokemon/random`);
    const data: Pokemon = await response.json();
    console.log(data);
    return data;
}

function TrainerBlock(name: string, imageUrl: string) {
    return (
        <div className="hover:bg-purple-600 flex flex-col items-center pt-5">
            <img src={imageUrl}
                className="object-contain h-64 w-64"></img>
            <p className="text-white">{name}</p>
        </div>
    );
}

function PokemonBlock(pokemon: Pokemon) {
    return (
        <div className="hover:bg-purple-600 flex flex-col items-center">
            <Link href={`/pokemon/${pokemon.id}`}>
                <img src={pokemon.artwork}
                    className="object-contain h-64 w-64"></img>
            </Link>
            <p className="text-white">{pokemon.nickname}</p>
            <p className="text-white">Level {pokemon.level}</p>
        </div>
    );
}

function DummyPokemonBlock(pokemon: Pokemon) {
    return (
        <div className="hover:bg-purple-600 flex flex-col items-center">
            <img src={pokemon.artwork}
                className="object-contain h-64 w-64 brightness-0"></img>
            <p className="text-white">???</p>
            <p className="text-white">Level ???</p>
        </div>
    );
}

export default async function PokemonPage({ params }: any) {
    const trainer = await getTrainer(params.trainer);
    var pokemonData = await getTrainerPokemon(params.trainer);
    var pokemonBlocks: JSX.Element[] = pokemonData.pokemon.map(PokemonBlock);

    while (pokemonBlocks.length < 6) {
        var randomBlock = DummyPokemonBlock(await getRandomPokemon());
        pokemonBlocks.push(randomBlock)
    }

    return (
        <div>
            <div className="pt-5 grid grid-cols-2">
                {pokemonBlocks[0]}
                {pokemonBlocks[1]}
            </div>
            <div className="grid grid-cols-3">
                {pokemonBlocks[2]}
                {TrainerBlock(trainer.name, trainer.image)}
                {pokemonBlocks[3]}
            </div>
            <div className="grid grid-cols-2">
                {pokemonBlocks[4]}
                {pokemonBlocks[5]}
            </div>
        </div>
    );
}

import Link from "next/link";

export default function HomePage() {
    return (
        <div className="pt-10">
            <Link href="/trainers/Melo">
                <h1 className="font-pokemon text-center text-white hover:text-yellow-400 text-6xl hover:text-7xl">
                    Melo's Pokémon Adventure
                </h1>
            </Link>
            <p className="text-center text-5xl pt-10">
                😉
            </p>
        </div>
    );
}

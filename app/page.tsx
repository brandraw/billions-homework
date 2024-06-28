import BillionsItem from "./_components/billions-item";

async function getBillions() {
  const result = await fetch("https://billions-api.nomadcoders.workers.dev/");

  return await result.json();
}

export default async function Home() {
  const billions = await getBillions();

  console.log(billions);

  return (
    <main>
      <div className="py-14">
        <div className="max-w-screen-lg w-full mx-auto px-5">
          <div className="grid grid-cols-4 gap-5">
            {billions.map((a: any, i: number) => (
              <BillionsItem {...a} key={i} />
            ))}
          </div>
        </div>
      </div>
    </main>
  );
}

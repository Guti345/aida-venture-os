import StartupDetail from './StartupDetail'

export async function generateStaticParams() {
  return [
    { name: 'FinStack' },
    { name: 'LogiFlow' },
    { name: 'MediSync' },
    { name: 'CreditIA' },
    { name: 'AgriSense' },
  ]
}

export default function StartupDetailPage({ params }: { params: { name: string } }) {
  return <StartupDetail name={params.name} />
}

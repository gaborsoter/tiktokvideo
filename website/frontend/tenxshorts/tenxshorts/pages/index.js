import { useState, useEffect } from 'react'
import { withAuthenticator, useAuthenticator } from '@aws-amplify/ui-react'
import { Storage } from "aws-amplify"
import { FileUploader, Collection, Image, Button } from '@aws-amplify/ui-react'
import HeroLayout1 from "@/src/ui-components/HeroLayout1"
import NavBar from "@/src/ui-components/NavBar"
import XHeroLayout2 from "@/src/ui-components/XHeroLayout2"
import Features2x2 from "@/src/ui-components/Features2x2"
import Demo from "@/src/ui-components/Demo"
import Features4x1 from "@/src/ui-components/Features4x1"
import MarketingFooter from "@/src/ui-components/MarketingFooter"

function Home() {
  const [imageKeys, setImageKeys] = useState([])
  const [images, setImages] = useState([])
  const {signOut} = useAuthenticator((context)=>[context.signOut])

  const fetchImages = async () => {
    const {results} = await Storage.list('', {level: 'private'}) 
    setImageKeys(results)
    const s3Images = await Promise.all(
      results.map(
        async (image) => await Storage.get(image.key, {level: 'private'})
      )
    )
    setImages(s3Images)
  }

  useEffect(() => {
    fetchImages()
  }, [])

  const onSuccess = (event) => {
    fetchImages()
  }


  return (
      <div>    
        <FileUploader
          accessLevel="private"
          acceptedFileTypes={["image/*"]}
          variation="drop"
          onSuccess={onSuccess}
        />
        <Collection
          items={images}
          type = "grid"
          padding = "2rem"
          maxWidth="1100px"
          margin = "0 auto"
          justifyContent={"center"}
          templateColumns={{
            base: "minmax(0, 500px)",
            medium: "repeat(2, minmax(0, 1fr))",
            large: "repeat(3, minmax(0, 1fr))",
          }}
          gap="small"
        >
          {(item, index) => (
            <div key = {index}>
              <Image src={item} alt=""/>
              <h2>{index}</h2>
            </div>
          )}
        </Collection>
        <Button onClick={signOut}>Sign out</Button>
        <NavBar width='100%'/>
        <XHeroLayout2 width='100%'/>
        <Features4x1 width='100%'/>
        <Demo width='100%'/>.
        <Features2x2 width='100%'/>
        <MarketingFooter width='100%'/>
      </div>
  )
}

export default withAuthenticator(Home)
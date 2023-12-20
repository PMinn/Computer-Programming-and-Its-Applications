import { Skeleton, Card, CardHeader, CardBody, CardFooter, Image, Button, Input, Progress, Table, TableHeader, TableBody, TableColumn, TableRow, TableCell } from "@nextui-org/react";
import { useState, useEffect, useCallback, useMemo } from "react";
import { SearchIcon } from "@/icons/SearchIcon";

export default function Home() {
  const host = ''
  const [data, setData] = useState([]);
  const [images, setImages] = useState([]);
  const [filterValue, setFilterValue] = useState("");
  const [selectedKeys, setSelectedKeys] = useState(new Set([]));
  const [isLoaded, setIsLoaded] = useState(false);
  const hasSearchFilter = Boolean(filterValue);

  useEffect(() => {
    fetch(`${host}/static/universityList.json`)
      .then(res => res.json())
      .then(setData)
  }, [])

  function executeAnalysis() {
    setIsLoaded(true)
    fetch(`${host}/api/analysis`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify([...selectedKeys].map(value => data.find(d => d.school.value == value)))
    })
      .then(res => res.json())
      .then(res => {
        console.log(res)
        let t = new Date().getTime();
        setImages([`${host}/static/count.jpg?t=${t}`, `${host}/static/cause.jpg?t=${t}`, `${host}/static/age.jpg?t=${t}`])
      })
      .finally(() => setIsLoaded(false))
  }

  const onSearchChange = useCallback((value) => {
    if (value) {
      setFilterValue(value);
    } else {
      setFilterValue("");
    }
  }, []);

  const filteredItems = useMemo(() => {
    let filteredData = [...data];
    if (hasSearchFilter) filteredData = filteredData.filter(d => d.school.text.includes(filterValue));
    return filteredData;
  }, [data, filterValue]);

  const onClear = useCallback(() => setFilterValue(""), [])

  return (
    <main className={`flex h-screen`}>
      <Card className='w-[25%] min-w-[450px] h-screen' radius='none'>
        <CardHeader>
          <Input
            isClearable
            className="w-full"
            placeholder="搜尋校名"
            startContent={<SearchIcon />}
            value={filterValue}
            onClear={() => onClear()}
            onValueChange={onSearchChange}
          />
        </CardHeader>
        <CardBody className="h-[80%] p-0">
          <Table
            removeWrapper
            hideHeader
            selectionMode="multiple"
            classNames={{
              base: "max-h-[100%] overflow-scroll",
              table: "min-h-[100%]",
            }}
            selectedKeys={selectedKeys}
            onSelectionChange={setSelectedKeys}
          >
            <TableHeader>
              <TableColumn>學校</TableColumn>
              <TableColumn>縣市</TableColumn>
            </TableHeader>
            <TableBody emptyContent={"No data found"} items={filteredItems}>
              {
                item => (
                  <TableRow key={item.school.value}>
                    <TableCell>{item.school.text}</TableCell>
                    <TableCell>{item.city.text}</TableCell>
                  </TableRow>
                )}
            </TableBody>
          </Table>
        </CardBody>
        <CardFooter>
          <Button
            isLoading={isLoaded}
            color='primary'
            className="w-full"
            onClick={executeAnalysis}
          >分析</Button>
        </CardFooter>
      </Card>

      <div className='grow overflow-y-scroll h-screen relative'>
        <div className="w-full py-5 h-full flex flex-col items-center">
          {
            images.map(image => (
              <div className="w-[90%] h-[50vh] flex justify-center items-center bg-white rounded-large mb-5">
                <Image className="w-full  h-full object-contain" src={image} disableSkeleton={true} />
              </div>
            ))
          }
        </div>
      </div>
    </main>
  )
}

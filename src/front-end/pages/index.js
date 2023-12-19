import { Skeleton, Card, CardHeader, CardBody, CardFooter, Image, Button, Input, Progress, Table, TableHeader, TableBody, TableColumn, TableRow, TableCell } from "@nextui-org/react";
import { useState, useEffect, useCallback, useMemo } from "react";
import { SearchIcon } from "@/icons/SearchIcon";

export default function Home() {
  const host = 'http://localhost:8088'
  const [data, setData] = useState([]);
  const [filterValue, setFilterValue] = useState("");
  const hasSearchFilter = Boolean(filterValue);

  useEffect(() => {
    fetch(`${host}/static/universityList.json`)
      .then(res => res.json())
      .then(setData)
  }, [])

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
      <Card className='w-[25%] h-screen' radius='none'>
        <CardBody className="h-[80%]">
          <Table
            hideHeader
            bottomContentPlacement="outside"
            selectionMode="multiple"
            topContent={(
              <div className="flex flex-col gap-4">
                <div className="flex justify-between gap-3 items-end">
                  <Input
                    isClearable
                    className="w-full"
                    placeholder="搜尋校名"
                    startContent={<SearchIcon />}
                    value={filterValue}
                    onClear={() => onClear()}
                    onValueChange={onSearchChange}
                  />
                </div>
              </div>
            )}
            classNames={{
              base: "max-h-[100%] overflow-scroll",
              table: "min-h-[100%]",
            }}
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
            // isLoading={isLoaded}
            color='primary'
            className="w-full"
          // onClick={executeSimulation}
          >分析</Button>
        </CardFooter>
      </Card>

      <div className='grow overflow-y-scroll h-screen relative'>
        {/* <Progress color="success" value={progress} className='sticky top-0 left-0 z-10' /> */}
        <div className="px-10 w-full">
          <div className='flex justify-between flex-wrap items-start mt-3 z-0 px-5'>
            <h2 className='w-[30%] font-bold text-xl m-2'></h2>
            <h2 className='w-[30%] font-bold text-xl m-2'></h2>
            <h2 className='w-[30%] font-bold text-xl m-2'></h2>

          </div>

        </div>
      </div>
    </main>
  )
}

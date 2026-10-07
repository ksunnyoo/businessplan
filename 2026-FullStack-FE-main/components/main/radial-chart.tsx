"use client"

import { BadgeCheck } from "lucide-react"
import { Label, PolarAngleAxis, PolarRadiusAxis, RadialBar, RadialBarChart } from "recharts"

import { Card, CardContent, CardFooter } from "@/components/ui/card"
import { ChartContainer, type ChartConfig } from "@/components/ui/chart"

const MAX_SCORE = 100

const chartConfig = {
    score: { label: "합격 지수", color: "var(--chart-2)" },
} satisfies ChartConfig

function RadialChart({ score = 83.5 }: { score?: number }) {
    const chartData = [{ name: "score", score }]

    return (
        <Card className="flex flex-col">
            <CardContent className="flex flex-1 flex-col items-center pb-0">
                <ChartContainer config={chartConfig} className="mx-auto aspect-square w-full max-w-[250px]">
                    <RadialBarChart data={chartData} startAngle={180} endAngle={0} innerRadius={80} outerRadius={110}>
                        {/* 핵심: 각도 축의 범위를 0~100으로 고정 */}
                        <PolarAngleAxis type="number" domain={[0, MAX_SCORE]} tick={false} />
                        <RadialBar
                            dataKey="score"
                            fill="var(--color-score)"
                            cornerRadius={5}
                            background={{ fill: "var(--muted)" }}
                        />
                        <PolarRadiusAxis tick={false} tickLine={false} axisLine={false}>
                            <Label
                                content={({ viewBox }) => {
                                    if (viewBox && "cx" in viewBox && "cy" in viewBox) {
                                        return (
                                            <text x={viewBox.cx} y={viewBox.cy} textAnchor="middle">
                                                <tspan x={viewBox.cx} y={(viewBox.cy || 0) - 16} className="fill-foreground text-4xl font-bold">
                                                    {score}
                                                </tspan>
                                                <tspan className="fill-muted-foreground text-lg">/{MAX_SCORE}</tspan>
                                                <tspan x={viewBox.cx} y={(viewBox.cy || 0) + 12} className="fill-muted-foreground text-sm">
                                                    종합 서면 합격 지수
                                                </tspan>
                                            </text>
                                        )
                                    }
                                }}
                            />
                        </PolarRadiusAxis>
                    </RadialBarChart>
                </ChartContainer>

                <div className="-mt-22 flex items-center gap-1 rounded-full bg-green-900/50 px-2 py-1">
                    <BadgeCheck size={13} className="text-green-500" />
                    <span className="mt-px text-xs font-semibold text-green-500">서면 심사 통과 안정권 (상위 TOP 12%)</span>
                </div>
            </CardContent>
            <CardFooter>
                <div className="flex w-full items-center justify-center gap-2 text-neutral-400">
                    <span>심사 가이드 라인 v2026. 10</span>
                    &middot;
                    <span>최근 진단: 3분 전(v1.4)</span>
                </div>
            </CardFooter>
        </Card>
    )
}

export default RadialChart
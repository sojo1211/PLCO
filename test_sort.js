const http = require('http');

function getPositionTier(posDetail, posCode) {
  const d = (posDetail || '').toLowerCase()
  const c = (posCode || '').toUpperCase()

  if (c === 'GK' || d.includes('goalkeeper')) return 0  // GK
  if (d.includes('center back') || d.includes('left back') || d.includes('right back')) return 1
  if (d.includes('defensive mid') || d.includes('wingback')) return 2
  if (d.includes('central mid')) return 3
  if (d.includes('attacking mid') || d.includes('winger')) return 4
  if (d.includes('striker') || d.includes('forward') || d.includes('center forward')) return 5
  if (c === 'DF') return 1
  if (c === 'MF') return 3
  if (c === 'FW') return 5
  return 3;
}

function getLateralOrder(posDetail) {
  const d = (posDetail || '').toLowerCase()
  if (d.includes('left')) return 1
  if (d.includes('center') || d.includes('central') || d.includes('striker')) return 2
  if (d.includes('right')) return 3
  return 2
}

function sortStartersToFormation(starters, formationStr) {
  const formation = (formationStr || '4-4-2').split('-').map(Number)
  if (!formation.every(n => !isNaN(n) && n > 0)) return starters

  const lineSlots = formation.map(n => n)

  const sorted = [...starters].sort((a, b) => {
    const tA = getPositionTier(a.position_detail, a.position)
    const tB = getPositionTier(b.position_detail, b.position)
    if (tA !== tB) return tA - tB
    return getLateralOrder(a.position_detail) - getLateralOrder(b.position_detail)
  })

  const gk = sorted.find(p => getPositionTier(p.position_detail, p.position) === 0)
  const outfield = sorted.filter(p => getPositionTier(p.position_detail, p.position) !== 0)

  const result = gk ? [gk] : []
  let playerIdx = 0
  for (let lineIdx = 0; lineIdx < lineSlots.length; lineIdx++) {
    const count = lineSlots[lineIdx]
    const linePlayers = outfield.slice(playerIdx, playerIdx + count)
    linePlayers.sort((a, b) => getLateralOrder(a.position_detail) - getLateralOrder(b.position_detail))
    result.push(...linePlayers)
    playerIdx += count
  }

  while (playerIdx < outfield.length) {
    result.push(outfield[playerIdx])
    playerIdx++
  }

  return result
}

function getHorizLayout(formationStr, side) {
  const defaultFormation = [4, 4, 2]
  let lines = defaultFormation
  if (formationStr) {
    const parts = formationStr.split('-').map(Number)
    if (parts.length > 0 && parts.every(n => !isNaN(n))) {
      lines = parts
    }
  }

  const positions = []
  positions.push({ x: side === 'home' ? 3 : 97, y: 50, isGK: true })

  const numLines = lines.length
  lines.forEach((count, lineIdx) => {
    const xPct = side === 'home' 
      ? 10 + (lineIdx / (numLines - 1 || 1)) * 38
      : 90 - (lineIdx / (numLines - 1 || 1)) * 38
    for (let i = 0; i < count; i++) {
      let yPct = 50
      if (count > 1) {
        yPct = 10 + (i / (count - 1)) * 80
      }
      positions.push({ x: xPct, y: yPct })
    }
  })

  return positions.slice(0, 11)
}

http.get('http://localhost:8000/api/fixtures/1/lineups', (res) => {
  let body = '';
  res.on('data', chunk => body += chunk);
  res.on('end', () => {
    const data = JSON.parse(body);
    
    // PSG (home)
    const homeLineup = data.filter(p => p.team_name === 'PSG');
    const homeFormation = homeLineup.find(p => p.formation)?.formation || '4-4-2';
    const homeStarters = sortStartersToFormation(homeLineup.filter(p => p.status?.toLowerCase() === 'starting'), homeFormation);
    const homePos = getHorizLayout(homeFormation, 'home');
    
    console.log("PSG Mapping (Home, Formation:", homeFormation, "):");
    homePos.forEach((pos, i) => {
      const p = homeStarters[i];
      console.log(`  Slot ${i}: Pos={x:${pos.x.toFixed(1)}, y:${pos.y.toFixed(1)}, gk:${!!pos.isGK}} => Player=${p ? p.player_name : 'UNDEFINED'} (jersey: ${p ? p.jersey_number : 'N/A'}, position: ${p ? p.position : 'N/A'})`);
    });

    console.log("\n=====================================\n");

    // Monaco (away)
    const awayLineup = data.filter(p => p.team_name === 'AS_Monaco');
    const awayFormation = awayLineup.find(p => p.formation)?.formation || '4-4-2';
    const awayStarters = sortStartersToFormation(awayLineup.filter(p => p.status?.toLowerCase() === 'starting'), awayFormation);
    const awayPos = getHorizLayout(awayFormation, 'away');

    console.log("Monaco Mapping (Away, Formation:", awayFormation, "):");
    awayPos.forEach((pos, i) => {
      const p = awayStarters[i];
      console.log(`  Slot ${i}: Pos={x:${pos.x.toFixed(1)}, y:${pos.y.toFixed(1)}, gk:${!!pos.isGK}} => Player=${p ? p.player_name : 'UNDEFINED'} (jersey: ${p ? p.jersey_number : 'N/A'}, position: ${p ? p.position : 'N/A'})`);
    });
  });
}).on('error', err => console.error(err));
